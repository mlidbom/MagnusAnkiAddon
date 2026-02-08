using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Collection;

public class SentenceCollection
{
    private readonly IBackendNoteCreator _backendNoteCreator;
    internal readonly SentenceCache Cache;
    public IAnkiNoteUpdateHandler AnkiSyncHandler => Cache;

    public SentenceCollection(IBackendNoteCreator backendNoteCreator)
    {
        _backendNoteCreator = backendNoteCreator;
        Cache = new SentenceCache();
    }

    public List<SentenceNote> PotentiallyMatchingVocab(VocabNote vocab)
    {
        List<string> searchStrings;
        if (vocab.MatchingConfiguration.RequiresForbids.Surface.IsRequired)
        {
            searchStrings = vocab.Forms.AllList();
        }
        else
        {
            searchStrings = vocab.Conjugator.GetStemsForAllForms()
                .Concat(vocab.Forms.AllList())
                .ToList();
        }

        var questions = All().Select(it => it.GetQuestion()).ToList();
        var matching = questions
            .Where(q => searchStrings.Any(s => q.Contains(s)))
            .Distinct()
            .ToList();

        return matching
            .SelectMany(q => Cache.WithQuestion(q))
            .Distinct()
            .ToList();
    }

    public List<SentenceNote> SentencesWithSubstring(string substring)
    {
        return Cache.All().Where(s => s.GetQuestion().Contains(substring)).ToList();
    }

    public List<SentenceNote> All() => Cache.All();

    public SentenceNote? WithIdOrNone(long noteId) => Cache.WithIdOrNone(noteId);

    public List<SentenceNote> WithQuestion(string question) => Cache.WithQuestion(question);

    public List<SentenceNote> WithVocab(VocabNote vocabNote)
    {
        var matches = Cache.WithVocab(vocabNote);
        var question = vocabNote.GetQuestion();
        // TODO: isn't this check redundant, won't the match have been removed during indexing?
        return matches.Where(match => !match.Configuration.IncorrectMatches.Words().Contains(question)).ToList();
    }

    public List<SentenceNote> WithVocabOwnedForm(VocabNote vocabNote)
    {
        var question = vocabNote.GetQuestion();
        return vocabNote.Forms.NotOwnedByOtherVocab()
            .SelectMany(form => Cache.WithVocabForm(form))
            .Distinct()
            .Where(match => !match.Configuration.IncorrectMatches.Words().Contains(question))
            .ToList();
    }

    public List<SentenceNote> WithVocabMarkedInvalid(VocabNote vocabNote)
    {
        return Cache.WithUserMarkedInvalidVocab(vocabNote.Question.DisambiguationName);
    }

    public List<SentenceNote> WithHighlightedVocab(VocabNote vocabNote)
    {
        if (vocabNote.Question.IsDisambiguated)
        {
            return Cache.WithUserHighlightedVocab(vocabNote.Question.DisambiguationName);
        }
        return vocabNote.Forms.AllSet()
            .SelectMany(form => Cache.WithUserHighlightedVocab(form))
            .ToList();
    }
    
    public List<SentenceNote> WithForm(string form) => Cache.WithVocabForm(form);
    
    public List<SentenceNote> WithUserHighlightedVocab(string form) => Cache.WithUserHighlightedVocab(form);
    
    public List<SentenceNote> WithUserMarkedInvalidVocab(string form) => Cache.WithUserMarkedInvalidVocab(form);

    public void Add(SentenceNote note)
    {
        _backendNoteCreator.CreateSentence(note, () => Cache.AddToCache(note));
    }
}

public class SentenceSnapshot : CachedNote
{
    public string[] Words { get; }
    public long[] DetectedVocab { get; }
    public string[] UserHighlightedVocab { get; }
    public string[] MarkedIncorrectVocab { get; }

    public SentenceSnapshot(SentenceNote note) : base(note)
    {
        Words = note.GetWords().ToArray();
        DetectedVocab = note.ParsingResult.Get().MatchedVocabIds.ToArray();
        UserHighlightedVocab = note.Configuration.HighlightedWords.ToArray();
        MarkedIncorrectVocab = note.Configuration.IncorrectMatches.Words().ToArray();
    }
}

public class SentenceCache : NoteCache<SentenceNote, SentenceSnapshot>
{
    private readonly Dictionary<string, HashSet<SentenceNote>> _byVocabForm = new();
    private readonly Dictionary<string, List<SentenceNote>> _byUserHighlightedVocab = new();
    private readonly Dictionary<string, List<SentenceNote>> _byUserMarkedInvalidVocab = new();
    private readonly Dictionary<long, HashSet<SentenceNote>> _byVocabId = new();

    public SentenceCache() : base(typeof(SentenceNote), (services, data) => new SentenceNote(services, data))
    {
    }

    protected override SentenceSnapshot CreateSnapshot(SentenceNote note)
    {
        return new SentenceSnapshot(note);
    }

    public List<SentenceNote> WithVocab(VocabNote vocab)
    {
        return _byVocabId.TryGetValue(vocab.GetId(), out var notes) ? notes.ToList() : new List<SentenceNote>();
    }

    public List<SentenceNote> WithVocabForm(string form)
    {
        return _byVocabForm.TryGetValue(form, out var notes) ? notes.ToList() : new List<SentenceNote>();
    }

    public List<SentenceNote> WithUserHighlightedVocab(string form)
    {
        return _byUserHighlightedVocab.TryGetValue(form, out var notes) ? notes : new List<SentenceNote>();
    }

    public List<SentenceNote> WithUserMarkedInvalidVocab(string form)
    {
        return _byUserMarkedInvalidVocab.TryGetValue(form, out var notes) ? notes : new List<SentenceNote>();
    }

    private static void RemoveFirstNoteWithId(List<SentenceNote> noteList, long id)
    {
        for (var i = 0; i < noteList.Count; i++)
        {
            if (noteList[i].GetId() == id)
            {
                noteList.RemoveAt(i);
                return;
            }
        }
        throw new Exception($"Could not find note with id {id} in list");
    }

    protected override void InheritorRemoveFromCache(SentenceNote note, SentenceSnapshot snapshot)
    {
        var id = snapshot.Id;

        foreach (var vocabForm in snapshot.Words)
        {
            if (_byVocabForm.TryGetValue(vocabForm, out var set))
            {
                set.Remove(note);
            }
        }
        foreach (var vocabForm in snapshot.UserHighlightedVocab)
        {
            if (_byUserHighlightedVocab.TryGetValue(vocabForm, out var list))
            {
                RemoveFirstNoteWithId(list, id);
            }
        }
        foreach (var vocabForm in snapshot.MarkedIncorrectVocab)
        {
            if (_byUserMarkedInvalidVocab.TryGetValue(vocabForm, out var list))
            {
                RemoveFirstNoteWithId(list, id);
            }
        }
        foreach (var vocabId in snapshot.DetectedVocab)
        {
            if (_byVocabId.TryGetValue(vocabId, out var set))
            {
                set.Remove(note);
            }
        }
    }

    protected override void InheritorAddToCache(SentenceNote note, SentenceSnapshot snapshot)
    {
        foreach (var vocabForm in snapshot.Words)
        {
            if (!_byVocabForm.ContainsKey(vocabForm))
            {
                _byVocabForm[vocabForm] = new HashSet<SentenceNote>();
            }
            _byVocabForm[vocabForm].Add(note);
        }
        foreach (var vocabForm in snapshot.UserHighlightedVocab)
        {
            if (!_byUserHighlightedVocab.ContainsKey(vocabForm))
            {
                _byUserHighlightedVocab[vocabForm] = new List<SentenceNote>();
            }
            _byUserHighlightedVocab[vocabForm].Add(note);
        }
        foreach (var vocabForm in snapshot.MarkedIncorrectVocab)
        {
            if (!_byUserMarkedInvalidVocab.ContainsKey(vocabForm))
            {
                _byUserMarkedInvalidVocab[vocabForm] = new List<SentenceNote>();
            }
            _byUserMarkedInvalidVocab[vocabForm].Add(note);
        }
        foreach (var vocabId in snapshot.DetectedVocab)
        {
            if (!_byVocabId.ContainsKey(vocabId))
            {
                _byVocabId[vocabId] = new HashSet<SentenceNote>();
            }
            _byVocabId[vocabId].Add(note);
        }
    }
}
