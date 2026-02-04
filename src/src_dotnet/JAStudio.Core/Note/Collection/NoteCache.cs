using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Note.Collection;

public class CachedNote
{
    public int Id { get; }
    public string Question { get; }

    public CachedNote(JPNote note)
    {
        Id = note.GetId();
        Question = note.GetQuestion();
    }
}

public abstract class NoteCacheBase<TNote> where TNote : JPNote
{
    private readonly Func<JPNoteData, TNote> _noteConstructor;
    private readonly Type _noteType;
    protected readonly Dictionary<int, TNote> _byId = new();
    private readonly List<Action<TNote>> _updateListeners = new();

    protected NoteCacheBase(Type cachedNoteType, Func<JPNoteData, TNote> noteConstructor)
    {
        _noteConstructor = noteConstructor;
        _noteType = cachedNoteType;
    }

    public void OnNoteUpdated(Action<TNote> listener)
    {
        _updateListeners.Add(listener);
    }

    public TNote? WithIdOrNone(int noteId)
    {
        return _byId.TryGetValue(noteId, out var note) ? note : null;
    }

    public void AnkiNoteUpdated(TNote note)
    {
        RefreshInCache(note);
    }

    public void JpNoteUpdated(TNote note)
    {
        RefreshInCache(note);
        NotifyUpdateListeners(note);
    }

    private void NotifyUpdateListeners(TNote note)
    {
        foreach (var listener in _updateListeners)
        {
            listener(note);
        }
    }

    private void RefreshInCache(TNote note)
    {
        RemoveFromCache(note);
        AddToCache(note);
    }

    public void InitFromList(List<JPNoteData> allNotes)
    {
        if (allNotes.Count > 0)
        {
            using var scope = TaskRunner.Current($"Pushing {_noteType.Name} notes into cache");
            var runner = TaskRunner.GetCurrent()!;
            runner.ProcessWithProgress(
                allNotes,
                noteData => { AddToCacheFromData(noteData); return 0; },
                $"Pushing {_noteType.Name} notes into cache");
        }
    }

    private void AddToCacheFromData(JPNoteData noteData)
    {
        AddToCache(_noteConstructor(noteData));
    }

    public abstract void RemoveFromCache(TNote note);
    public abstract void AddToCache(TNote note);

    public void SetStudyingStatuses(List<CardStudyingStatus> cardStatuses)
    {
        foreach (var status in cardStatuses)
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
    private readonly Dictionary<string, List<TNote>> _byQuestion = new();
    private readonly Dictionary<int, TSnapshot> _snapshotById = new();
    private readonly HashSet<int> _deleted = new();
    private bool _flushing;

    protected NoteCache(Type cachedNoteType, Func<JPNoteData, TNote> noteConstructor)
        : base(cachedNoteType, noteConstructor)
    {
    }

    public List<TNote> All()
    {
        return _byId.Values.ToList();
    }

    public List<TNote> WithQuestion(string question)
    {
        return _byQuestion.TryGetValue(question, out var notes) ? notes : new List<TNote>();
    }

    protected abstract TSnapshot CreateSnapshot(TNote note);
    protected abstract void InheritorRemoveFromCache(TNote note, TSnapshot snapshot);
    protected abstract void InheritorAddToCache(TNote note, TSnapshot snapshot);

    public override void RemoveFromCache(TNote note)
    {
        var id = note.GetId();
        if (id == 0) throw new InvalidOperationException("Cannot remove note without ID");

        var cached = _snapshotById[id];
        _snapshotById.Remove(id);
        _byId.Remove(id);
        
        if (_byQuestion.TryGetValue(cached.Question, out var questionList))
        {
            questionList.Remove(note);
        }
        
        InheritorRemoveFromCache(note, cached);
    }

    public override void AddToCache(TNote note)
    {
        var id = note.GetId();
        if (id == 0) throw new InvalidOperationException("Cannot add note without ID");

        var snapshot = CreateSnapshot(note);
        _snapshotById[id] = snapshot;
        _byId[id] = note;
        
        if (!_byQuestion.ContainsKey(snapshot.Question))
        {
            _byQuestion[snapshot.Question] = new List<TNote>();
        }
        _byQuestion[snapshot.Question].Add(note);
        
        InheritorAddToCache(note, snapshot);
    }
}
