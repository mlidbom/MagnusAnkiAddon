using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Compze.Utilities.SystemCE.ThreadingCE.ResourceAccess;
using JAStudio.Core.Anki;
using JAStudio.PythonInterop;

namespace JAStudio.Core.Note.Collection;

public class CachedNote
{
   public NoteId Id { get; }
   public string Question { get; }

   public CachedNote(JPNote note)
   {
      Id = note.GetId();
      Question = note.GetQuestion();
   }
}

public abstract class NoteCacheBase<TNote> : IAnkiNoteUpdateHandler where TNote : JPNote
{
   readonly Func<NoteServices, NoteData, TNote> _noteConstructor;
   readonly Type _noteType;
   protected readonly Dictionary<NoteId, TNote> _byId = new();
   readonly List<Action<TNote>> _updateListeners = new();
   readonly Dictionary<long, NoteId> _ankiIdToNoteId = new();
   readonly Dictionary<NoteId, long> _noteIdToAnkiId = new();
   NoteServices? _noteServices;

   protected NoteCacheBase(Type cachedNoteType, Func<NoteServices, NoteData, TNote> noteConstructor)
   {
      _noteConstructor = noteConstructor;
      _noteType = cachedNoteType;
   }

   public void SetNoteServices(NoteServices noteServices)
   {
      _noteServices = noteServices;
   }

   NoteServices RequireServices() => _noteServices ?? throw new InvalidOperationException($"NoteServices not set on {_noteType.Name} cache. Call SetNoteServices first.");

   public void OnNoteUpdated(dynamic listener)
   {
      Action<TNote> callback = PythonDotNetShim.Action.ToDotNet<TNote>(listener);
      _updateListeners.Add(callback);
   }

   public TNote? WithIdOrNone(NoteId noteId) => _byId.TryGetValue(noteId, out var note) ? note : null;

   /// <summary>
   /// Registers the mapping between an Anki note ID and the domain NoteId.
   /// Called during bulk loading and when notes are added via Anki.
   /// </summary>
   public void RegisterAnkiIdMapping(long ankiNoteId, NoteId noteId)
   {
      _ankiIdToNoteId[ankiNoteId] = noteId;
      _noteIdToAnkiId[noteId] = ankiNoteId;
   }

   /// <summary>Look up a note by its Anki long ID (uses the internal mapping).</summary>
   public TNote? WithAnkiIdOrNone(long ankiNoteId) =>
      _ankiIdToNoteId.TryGetValue(ankiNoteId, out var noteId) ? WithIdOrNone(noteId) : null;

   /// <summary>Converts an Anki long ID to the corresponding domain NoteId.</summary>
   public NoteId? AnkiIdToNoteId(long ankiNoteId) =>
      _ankiIdToNoteId.TryGetValue(ankiNoteId, out var noteId) ? noteId : null;

   /// <summary>Returns the Anki long note ID for the given domain NoteId.</summary>
   public long GetAnkiNoteId(NoteId noteId) =>
      _noteIdToAnkiId.TryGetValue(noteId, out var ankiId) ? ankiId : 0;

   public void AnkiNoteAdded(long ankiNoteId, NoteData data)
   {
      data.Id = CreateTypedId(Guid.NewGuid());
      _ankiIdToNoteId[ankiNoteId] = data.Id;
      _noteIdToAnkiId[data.Id] = ankiNoteId;
      var note = _noteConstructor(RequireServices(), data);
      using(note.RecursiveFlushGuard.PauseFlushing())
      {
         note.UpdateGeneratedData();
      }
      AddToCache(note);
   }

   public void AnkiNoteWillFlush(long ankiNoteId, NoteData data)
   {
      if(!_ankiIdToNoteId.TryGetValue(ankiNoteId, out var noteId)) return;
      var existing = WithIdOrNone(noteId);
      if(existing == null) return;
      if(existing.IsFlushing) return; // Our code initiated this flush, nothing to do

      data.Id = noteId;
      var note = _noteConstructor(RequireServices(), data);
      note.CopyStudyingStatusFrom(existing);
      using(note.RecursiveFlushGuard.PauseFlushing())
      {
         note.UpdateGeneratedData();
      }
      RefreshInCache(note);
      NotifyUpdateListeners(note);
   }

   public void AnkiNoteRemoved(long ankiNoteId)
   {
      if(!_ankiIdToNoteId.TryGetValue(ankiNoteId, out var noteId)) return;
      var existing = WithIdOrNone(noteId);
      if(existing != null)
      {
         RemoveFromCache(existing);
      }
      _ankiIdToNoteId.Remove(ankiNoteId);
      if(noteId != null) _noteIdToAnkiId.Remove(noteId);
   }

   /// <summary>Creates the correctly typed NoteId for this cache (VocabId, KanjiId, etc.)</summary>
   protected abstract NoteId CreateTypedId(Guid value);

   public void JpNoteUpdated(TNote note)
   {
      var existing = WithIdOrNone(note.GetId());
      if(existing != null)
      {
         RefreshInCache(note);
      }
      else
      {
         AddToCache(note);
      }
      NotifyUpdateListeners(note);
   }

   void NotifyUpdateListeners(TNote note)
   {
      foreach(var listener in _updateListeners)
      {
         listener(note);
      }
   }

   void RefreshInCache(TNote note)
   {
      RemoveFromCache(note);
      AddToCache(note);
   }

   public async Task LoadAsync()
   {
      var dbPath = AnkiFacade.Col.DbFilePath();

      using var runner = RequireServices().TaskRunner.Current($"Loading {_noteType.Name} notes from the anki db");
      var loadResult = await runner.RunOnBackgroundThreadAsync($"Fetching {_noteType.Name} notes from anki db", () => NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.FromType(_noteType)));

      // Build a temporary map from base NoteId → ankiId so we can re-register
      // with the typed NoteId (VocabId, KanjiId, etc.) after note construction.
      var baseIdToAnkiId = new Dictionary<Guid, long>();
      foreach(var (ankiId, noteId) in loadResult.AnkiIdMap)
      {
         baseIdToAnkiId[noteId.Value] = ankiId;
      }

      await runner.ProcessWithProgressAsync(loadResult.Notes, noteData =>
      {
         var note = _noteConstructor(RequireServices(), noteData);
         AddToCache(note);

         // Register mapping using the note's typed ID so record equality works in lookups.
         var typedId = note.GetId();
         if(baseIdToAnkiId.TryGetValue(typedId.Value, out var ankiId))
         {
            _ankiIdToNoteId[ankiId] = typedId;
            _noteIdToAnkiId[typedId] = ankiId;
         }
      }, "");
   }

   void AddToCacheFromData(NoteData noteData)
   {
      AddToCache(_noteConstructor(RequireServices(), noteData));
   }

   public abstract void RemoveFromCache(TNote note);
   public abstract void AddToCache(TNote note);

   public void SetStudyingStatuses(Dictionary<long, List<CardStudyingStatus>> statusesByAnkiId)
   {
      foreach(var (ankiId, statuses) in statusesByAnkiId)
      {
         var note = WithAnkiIdOrNone(ankiId);
         if(note != null)
         {
            foreach(var status in statuses)
               note.SetStudyingStatus(status);
         }
      }
   }
}

public abstract class NoteCache<TNote, TSnapshot> : NoteCacheBase<TNote>
   where TNote : JPNote
   where TSnapshot : CachedNote
{
   readonly IMonitorCE _monitor = IMonitorCE.WithDefaultTimeout();
   readonly Dictionary<string, List<TNote>> _byQuestion = new();
   readonly Dictionary<NoteId, TSnapshot> _snapshotById = new();

   protected NoteCache(Type cachedNoteType, Func<NoteServices, NoteData, TNote> noteConstructor)
      : base(cachedNoteType, noteConstructor) {}

   public List<TNote> All() => _byId.Values.ToList();

   public List<TNote> WithQuestion(string question) => _byQuestion.TryGetValue(question, out var notes) ? notes : new List<TNote>();

   protected abstract TSnapshot CreateSnapshot(TNote note);
   protected abstract void InheritorRemoveFromCache(TNote note, TSnapshot snapshot);
   protected abstract void InheritorAddToCache(TNote note, TSnapshot snapshot);

   public override void RemoveFromCache(TNote note) => _monitor.Update(() =>
   {
      var id = note.GetId();

      var cached = _snapshotById[id];
      _snapshotById.Remove(id);
      _byId.Remove(id);

      if(_byQuestion.TryGetValue(cached.Question, out var questionList))
      {
         questionList.Remove(note);
      }

      InheritorRemoveFromCache(note, cached);
   });

   public override void AddToCache(TNote note) => _monitor.Update(() =>
   {
      var id = note.GetId();

      // If already in cache, clean up old secondary indexes first (idempotent add)
      if(_snapshotById.TryGetValue(id, out var existingSnapshot))
      {
         _byId.Remove(id);
         _snapshotById.Remove(id);
         if(_byQuestion.TryGetValue(existingSnapshot.Question, out var existingQuestionList))
         {
            existingQuestionList.Remove(note);
         }
         InheritorRemoveFromCache(note, existingSnapshot);
      }

      var snapshot = CreateSnapshot(note);
      _snapshotById[id] = snapshot;
      _byId[id] = note;

      if(!_byQuestion.ContainsKey(snapshot.Question))
      {
         _byQuestion[snapshot.Question] = new List<TNote>();
      }

      _byQuestion[snapshot.Question].Add(note);

      InheritorAddToCache(note, snapshot);
   });
}
