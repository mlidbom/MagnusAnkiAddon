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
   readonly List<Action<TNote>> _deleteListeners = new();
   readonly NoteServices _noteServices;
   protected readonly IMonitorCE _monitor = IMonitorCE.WithDefaultTimeout();

   protected NoteCacheBase(Type cachedNoteType, Func<NoteServices, NoteData, TNote> noteConstructor, NoteServices noteServices)
   {
      _noteConstructor = noteConstructor;
      _noteType = cachedNoteType;
      _noteServices = noteServices;
   }

   public void OnNoteUpdated(dynamic listener)
   {
      Action<TNote> callback = PythonDotNetShim.Action.ToDotNet<TNote>(listener);
      _updateListeners.Add(callback);
   }

   public void OnNoteUpdated(Action<TNote> listener)
   {
      _updateListeners.Add(listener);
   }

   public void OnNoteDeleted(Action<TNote> listener)
   {
      _deleteListeners.Add(listener);
   }

   public TNote? WithIdOrNone(NoteId noteId) => _monitor.Read(() => WithIdOrNoneCore(noteId));
   protected TNote? WithIdOrNoneCore(NoteId noteId) => _byId.TryGetValue(noteId, out var note) ? note : null;

   /// <summary>Look up a note by its Anki long ID (uses the shared AnkiNoteIdMap).</summary>
   public TNote? WithAnkiIdOrNone(long ankiNoteId) =>
      _noteServices.AnkiNoteIdMap.FromAnkiId(ankiNoteId) is {} noteId ? WithIdOrNone(noteId) : null;

   TNote? WithAnkiIdOrNoneCore(long ankiNoteId) =>
      _noteServices.AnkiNoteIdMap.FromAnkiId(ankiNoteId) is {} noteId ? WithIdOrNoneCore(noteId) : null;

   /// <summary>Converts an Anki long ID to the corresponding domain NoteId.</summary>
   public NoteId? AnkiIdToNoteId(long ankiNoteId) =>
      _noteServices.AnkiNoteIdMap.FromAnkiId(ankiNoteId);

   /// <summary>Returns the Anki long note ID for the given domain NoteId.</summary>
   public long GetAnkiNoteId(NoteId noteId) =>
      _noteServices.AnkiNoteIdMap.ToAnkiId(noteId) ?? 0;

   public void AnkiNoteAdded(long ankiNoteId, NoteData data)
   {
      data.Id = CreateTypedId(Guid.NewGuid());
      _noteServices.AnkiNoteIdMap.Register(ankiNoteId, data.Id);
      var note = _noteConstructor(_noteServices, data);
      using(note.RecursiveFlushGuard.PauseFlushing())
      {
         note.UpdateGeneratedData();
      }

      AddToCache(note);
   }

   public void AnkiNoteWillFlush(long ankiNoteId, NoteData data)
   {
      var noteId = _noteServices.AnkiNoteIdMap.FromAnkiId(ankiNoteId);
      if(noteId == null) return;
      var existing = WithIdOrNone(noteId);
      if(existing == null) return;
      if(existing.IsFlushing) return; // Our code initiated this flush, nothing to do

      data.Id = noteId;
      var note = _noteConstructor(_noteServices, data);
      note.CopyStudyingStatusFrom(existing);
      using(note.RecursiveFlushGuard.PauseFlushing())
      {
         note.UpdateGeneratedData();
      }

      _monitor.Update(() => RefreshInCacheCore(note));
      NotifyUpdateListeners(note);
   }

   public void AnkiNoteRemoved(long ankiNoteId)
   {
      var noteId = _noteServices.AnkiNoteIdMap.FromAnkiId(ankiNoteId);
      if(noteId == null) return;
      TNote? removed = null;
      _monitor.Update(() =>
      {
         var existing = WithIdOrNoneCore(noteId);
         if(existing != null)
         {
            RemoveFromCacheCore(existing);
            removed = existing;
         }
      });

      if (removed != null)
         NotifyDeleteListeners(removed);

      _noteServices.AnkiNoteIdMap.Unregister(ankiNoteId);
   }

   /// <summary>Creates the correctly typed NoteId for this cache (VocabId, KanjiId, etc.)</summary>
   protected abstract NoteId CreateTypedId(Guid value);

   public void JpNoteUpdated(TNote note)
   {
      _monitor.Update(() =>
      {
         var existing = WithIdOrNoneCore(note.GetId());
         if(existing != null)
         {
            RefreshInCacheCore(note);
         } else
         {
            AddToCacheCore(note);
         }
      });

      NotifyUpdateListeners(note);
   }

   void NotifyUpdateListeners(TNote note)
   {
      foreach(var listener in _updateListeners)
      {
         listener(note);
      }
   }

   void NotifyDeleteListeners(TNote note)
   {
      foreach(var listener in _deleteListeners)
      {
         listener(note);
      }
   }

   void RefreshInCacheCore(TNote note)
   {
      RemoveFromCacheCore(note);
      AddToCacheCore(note);
   }

   public async Task LoadAsync()
   {
      var dbPath = AnkiFacade.Col.DbFilePath();
      if(dbPath == null) throw new InvalidOperationException("Anki collection database is not initialized yet");

      using var runner = _noteServices.TaskRunner.Current($"Loading {_noteType.Name} notes from the anki db");
      var loadResult = await runner.RunOnBackgroundThreadWithSpinningProgressDialogAsync($"Fetching {_noteType.Name} notes from anki db", () => NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.FromType(_noteType), NoteTypes.IdFactoryFromType(_noteType)));

      foreach(var (ankiId, noteId) in loadResult.AnkiIdMap)
      {
         _noteServices.AnkiNoteIdMap.Register(ankiId, noteId);
      }

      var notes = runner.ProcessWithProgress(loadResult.Notes, it => _noteConstructor(_noteServices, it), $"Constructing {_noteType.Name} notes");

      await runner.ProcessWithProgressAsync(notes, AddToCache, $"Pushing {_noteType.Name} notes into cache");
   }

   /// <summary>Removes all notes and ID mappings from the cache. Subclasses must override ClearInheritorIndexes to clear their custom indexes.</summary>
   public void Clear() => _monitor.Update(() =>
   {
      _byId.Clear();
      ClearInheritorIndexes();
   });

   protected abstract void ClearInheritorIndexes();

   /// <summary>Locked entry point: acquires the write lock and calls AddToCacheCore.</summary>
   public void AddToCache(TNote note) => _monitor.Update(() => AddToCacheCore(note));
   /// <summary>Locked entry point: acquires the write lock and calls RemoveFromCacheCore.</summary>
   public void RemoveFromCache(TNote note) => _monitor.Update(() => RemoveFromCacheCore(note));

   /// <summary>Adds the note to all indexes. Must be called under the write lock.</summary>
   protected abstract void AddToCacheCore(TNote note);
   /// <summary>Removes the note from all indexes. Must be called under the write lock.</summary>
   protected abstract void RemoveFromCacheCore(TNote note);

   public void SetStudyingStatuses(Dictionary<long, List<CardStudyingStatus>> statusesByAnkiId)
   {
      _monitor.Read(() =>
      {
         foreach(var (ankiId, statuses) in statusesByAnkiId)
         {
            var note = WithAnkiIdOrNoneCore(ankiId);
            if(note != null)
            {
               foreach(var status in statuses)
                  note.SetStudyingStatus(status);
            }
         }
      });
   }
}

public abstract class NoteCache<TNote, TSnapshot> : NoteCacheBase<TNote>
   where TNote : JPNote
   where TSnapshot : CachedNote
{
   readonly Dictionary<string, HashSet<TNote>> _byQuestion = new();
   readonly Dictionary<NoteId, TSnapshot> _snapshotById = new();

   protected NoteCache(Type cachedNoteType, Func<NoteServices, NoteData, TNote> noteConstructor, NoteServices noteServices)
      : base(cachedNoteType, noteConstructor, noteServices) {}

   public List<TNote> All() => _monitor.Read(() => _byId.Values.ToList());

   public List<TNote> WithQuestion(string question) => _monitor.Read(() => _byQuestion.TryGetValue(question, out var notes) ? notes.ToList() : new List<TNote>());

   protected abstract TSnapshot CreateSnapshot(TNote note);
   protected abstract void InheritorRemoveFromCache(TNote note, TSnapshot snapshot);
   protected abstract void InheritorAddToCache(TNote note, TSnapshot snapshot);

   protected override void ClearInheritorIndexes()
   {
      _byQuestion.Clear();
      _snapshotById.Clear();
      ClearDerivedIndexes();
   }

   /// <summary>Override in leaf caches to clear type-specific secondary indexes.</summary>
   protected abstract void ClearDerivedIndexes();

   protected override void RemoveFromCacheCore(TNote note)
   {
      var id = note.GetId();

      if(!_snapshotById.TryGetValue(id, out var cached))
         return;

      _snapshotById.Remove(id);
      _byId.Remove(id);

      if(_byQuestion.TryGetValue(cached.Question, out var questionList))
      {
         questionList.Remove(note);
      }

      InheritorRemoveFromCache(note, cached);
   }

   protected override void AddToCacheCore(TNote note)
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
         _byQuestion[snapshot.Question] = new HashSet<TNote>();
      }

      _byQuestion[snapshot.Question].Add(note);

      InheritorAddToCache(note, snapshot);
   }
}
