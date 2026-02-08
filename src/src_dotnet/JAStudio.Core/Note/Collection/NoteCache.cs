using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using JAStudio.Core.TaskRunners;
using JAStudio.PythonInterop;

namespace JAStudio.Core.Note.Collection;

public class CachedNote
{
   public long Id { get; }
   public string Question { get; }

   public CachedNote(JPNote note)
   {
      Id = note.GetId();
      Question = note.GetQuestion();
   }
}

public abstract class NoteCacheBase<TNote> where TNote : JPNote
{
   readonly Func<NoteServices, NoteData, TNote> _noteConstructor;
   readonly Type _noteType;
   protected readonly Dictionary<long, TNote> _byId = new();
   readonly List<Action<TNote>> _updateListeners = new();
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

   public TNote? WithIdOrNone(long noteId) => _byId.TryGetValue(noteId, out var note) ? note : null;

   public void AnkiNoteUpdated(TNote note)
   {
      RefreshInCache(note);
   }

   public void JpNoteUpdated(TNote note)
   {
      RefreshInCache(note);
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

   public void InitFromList(List<NoteData> allNotes)
   {
      if(allNotes.Count > 0)
      {
         var services = RequireServices();
         using var scope = services.TaskRunner.Current($"Pushing {_noteType.Name} notes into cache");
         scope.ProcessWithProgress(
            allNotes,
            noteData =>
            {
               AddToCacheFromData(noteData);
               return 0;
            },
            $"Pushing {_noteType.Name} notes into cache");
      }
   }

   /// <summary>
   /// Async version of <see cref="InitFromList"/> for parallel loading.
   /// Each call runs on its own thread via <see cref="Task.Run"/> so that
   /// <see cref="TaskRunner.Current"/> creates an independent scope and progress panel.
   /// Multiple concurrent calls display stacked progress rows automatically.
   /// </summary>
   public Task InitFromListAsync(List<NoteData> allNotes)
   {
      if(allNotes.Count == 0) return Task.CompletedTask;

      var services = RequireServices();
      var message = $"Pushing {_noteType.Name} notes into cache";
      return Task.Run(() =>
      {
         using var scope = services.TaskRunner.Current(message);
         scope.ProcessWithProgress(
            allNotes,
            noteData =>
            {
               AddToCacheFromData(noteData);
               return 0;
            },
            message);
      });
   }

   void AddToCacheFromData(NoteData noteData)
   {
      AddToCache(_noteConstructor(RequireServices(), noteData));
   }

   public abstract void RemoveFromCache(TNote note);
   public abstract void AddToCache(TNote note);

   public void SetStudyingStatuses(List<CardStudyingStatus> cardStatuses)
   {
      foreach(var status in cardStatuses)
      {
         var note = WithIdOrNone(status.NoteId);
         note?.SetStudyingStatus(status);
      }
   }
}

public abstract class NoteCache<TNote, TSnapshot> : NoteCacheBase<TNote>
   where TNote : JPNote
   where TSnapshot : CachedNote
{
   readonly Dictionary<string, List<TNote>> _byQuestion = new();
   readonly Dictionary<long, TSnapshot> _snapshotById = new();

   protected NoteCache(Type cachedNoteType, Func<NoteServices, NoteData, TNote> noteConstructor)
      : base(cachedNoteType, noteConstructor) {}

   public List<TNote> All() => _byId.Values.ToList();

   public List<TNote> WithQuestion(string question) => _byQuestion.TryGetValue(question, out var notes) ? notes : new List<TNote>();

   protected abstract TSnapshot CreateSnapshot(TNote note);
   protected abstract void InheritorRemoveFromCache(TNote note, TSnapshot snapshot);
   protected abstract void InheritorAddToCache(TNote note, TSnapshot snapshot);

   public override void RemoveFromCache(TNote note)
   {
      var id = note.GetId();
      if(id == 0) throw new InvalidOperationException("Cannot remove note without ID");

      var cached = _snapshotById[id];
      _snapshotById.Remove(id);
      _byId.Remove(id);

      if(_byQuestion.TryGetValue(cached.Question, out var questionList))
      {
         questionList.Remove(note);
      }

      InheritorRemoveFromCache(note, cached);
   }

   public override void AddToCache(TNote note)
   {
      var id = note.GetId();
      if(id == 0) throw new InvalidOperationException("Cannot add note without ID");

      var snapshot = CreateSnapshot(note);
      _snapshotById[id] = snapshot;
      _byId[id] = note;

      if(!_byQuestion.ContainsKey(snapshot.Question))
      {
         _byQuestion[snapshot.Question] = new List<TNote>();
      }

      _byQuestion[snapshot.Question].Add(note);

      InheritorAddToCache(note, snapshot);
   }
}
