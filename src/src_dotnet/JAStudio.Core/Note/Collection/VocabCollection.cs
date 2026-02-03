using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.Note.Collection;

public class VocabCollection
{
    private readonly IBackendNoteCreator _backendNoteCreator;
    internal readonly VocabCache Cache;

    public VocabCollection(IBackendNoteCreator backendNoteCreator)
    {
        _backendNoteCreator = backendNoteCreator;
        Cache = new VocabCache();
    }

    public bool IsWord(string form) => Cache.WithForm(form).Any();
    public List<VocabNote> All() => Cache.All();
    public VocabNote? WithIdOrNone(int noteId) => Cache.WithIdOrNone(noteId);
    public IEnumerable<VocabNote> WithDisambiguationName(string name) => Cache.WithDisambiguationName(name);
    public IEnumerable<VocabNote> WithForm(string form) => Cache.WithForm(form);
    public List<VocabNote> WithCompoundPart(string disambiguationName) => Cache.WithCompoundPart(disambiguationName);
    public List<VocabNote> DerivedFrom(string derivedFrom) => Cache.DerivedFrom(derivedFrom);
    public List<VocabNote> WithKanjiInMainForm(KanjiNote kanji) => Cache.WithKanjiInMainForm(kanji.GetQuestion());
    public List<VocabNote> WithKanjiInAnyForm(KanjiNote kanji) => Cache.WithKanjiInAnyForm(kanji.GetQuestion());
    public List<VocabNote> WithQuestion(string question) => Cache.WithQuestion(question);
    
    public IEnumerable<VocabNote> WithQuestionPreferDisambiguationName(string question)
    {
        return question.Contains(VocabNoteQuestion.DisambiguationMarker)
            ? Cache.WithDisambiguationName(question)
            : Cache.WithQuestion(question);
    }
    
    public List<VocabNote> WithReading(string reading) => Cache.WithReading(reading);
    public List<VocabNote> WithStem(string stem) => Cache.WithStem(stem);

    public List<VocabNote> WithFormPreferDisambiguationNameOrExactMatch(string form)
    {
        var withDisambiguationName = WithDisambiguationName(form).ToList();
        if (withDisambiguationName.Any())
            return withDisambiguationName;

        var matches = WithForm(form);
        var exactMatch = matches.Where(voc => voc.Question.Raw == form).ToList();
        var sequence = exactMatch.Any() ? exactMatch : matches;
        return sequence.Distinct().ToList();
    }

    public List<VocabNote> WithAnyFormInPreferDisambiguationNameOrExactMatch(List<string> forms)
    {
        return forms
            .SelectMany(WithFormPreferDisambiguationNameOrExactMatch)
            .Distinct()
            .ToList();
    }

    public List<VocabNote> WithAnyFormIn(List<string> forms)
    {
        return forms
            .SelectMany(WithForm)
            .Distinct()
            .ToList();
    }

    public List<VocabNote> WithAnyDisambiguationNameIn(IEnumerable<string> questions)
    {
        return questions
            .SelectMany(WithDisambiguationName)
            .ToList();
    }

    public void Add(VocabNote note)
    {
        _backendNoteCreator.CreateVocab(note, () => Cache.AddToCache(note));
    }
}

public class VocabSnapshot : CachedNote
{
    public string DisambiguationName { get; }
    public string[] Forms { get; }
    public string[] CompoundParts { get; }
    public string[] MainFormKanji { get; }
    public string[] AllKanji { get; }
    public string[] Readings { get; }
    public string DerivedFrom { get; }
    public string[] Stems { get; }

    public VocabSnapshot(VocabNote note) : base(note)
    {
        DisambiguationName = note.Question.DisambiguationName;
        Forms = note.Forms.AllList().ToArray();
        CompoundParts = Array.Empty<string>(); // TODO: Implement when compound parts are ported
        MainFormKanji = note.Kanji.ExtractMainFormKanji().ToArray();
        AllKanji = note.Kanji.ExtractAllKanji().ToArray();
        Readings = note.GetReadings().ToArray();
        DerivedFrom = string.Empty; // TODO: Implement when derived vocab is ported
        Stems = Array.Empty<string>(); // TODO: Implement when stems are ported
    }
}

public class VocabCache : NoteCache<VocabNote, VocabSnapshot>
{
    private readonly Dictionary<string, List<VocabNote>> _byDisambiguationName = new();
    private readonly Dictionary<string, List<VocabNote>> _byForm = new();
    private readonly Dictionary<string, List<VocabNote>> _byKanjiInMainForm = new();
    private readonly Dictionary<string, List<VocabNote>> _byKanjiInAnyForm = new();
    private readonly Dictionary<string, List<VocabNote>> _byCompoundPart = new();
    private readonly Dictionary<string, List<VocabNote>> _byDerivedFrom = new();
    private readonly Dictionary<string, List<VocabNote>> _byReading = new();
    private readonly Dictionary<string, List<VocabNote>> _byStem = new();

    public VocabCache() : base(typeof(VocabNote), data => new VocabNote(data))
    {
    }

    public IEnumerable<VocabNote> WithForm(string form)
    {
        return _byForm.TryGetValue(form, out var notes) ? notes : Enumerable.Empty<VocabNote>();
    }

    public IEnumerable<VocabNote> WithDisambiguationName(string form)
    {
        return _byDisambiguationName.TryGetValue(form, out var notes) ? notes : Enumerable.Empty<VocabNote>();
    }

    public List<VocabNote> WithCompoundPart(string disambiguationName)
    {
        var compoundParts = new HashSet<VocabNote>();

        void FetchParts(string partForm)
        {
            if (_byCompoundPart.TryGetValue(partForm, out var vocabList))
            {
                foreach (var vocab in vocabList)
                {
                    if (!compoundParts.Contains(vocab))
                    {
                        compoundParts.Add(vocab);
                        // TODO: Access vocab.question.disambiguation_name when implemented
                        // FetchParts(vocab.Question.DisambiguationName);
                    }
                }
            }
        }

        FetchParts(disambiguationName);

        return compoundParts.OrderBy(v => v.GetQuestion()).ToList();
    }

    public List<VocabNote> DerivedFrom(string form)
    {
        return _byDerivedFrom.TryGetValue(form, out var notes) ? notes : new List<VocabNote>();
    }

    public List<VocabNote> WithKanjiInMainForm(string kanji)
    {
        return _byKanjiInMainForm.TryGetValue(kanji, out var notes) ? notes : new List<VocabNote>();
    }

    public List<VocabNote> WithKanjiInAnyForm(string kanji)
    {
        return _byKanjiInAnyForm.TryGetValue(kanji, out var notes) ? notes : new List<VocabNote>();
    }

    public List<VocabNote> WithReading(string reading)
    {
        return _byReading.TryGetValue(reading, out var notes) ? notes : new List<VocabNote>();
    }

    public List<VocabNote> WithStem(string stem)
    {
        return _byStem.TryGetValue(stem, out var notes) ? notes : new List<VocabNote>();
    }

    protected override VocabSnapshot CreateSnapshot(VocabNote note)
    {
        return new VocabSnapshot(note);
    }

    private static void RemoveFirstNoteWithId(List<VocabNote> noteList, int id)
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

    protected override void InheritorRemoveFromCache(VocabNote note, VocabSnapshot snapshot)
    {
        var id = snapshot.Id;
        foreach (var form in snapshot.Forms)
        {
            if (_byForm.TryGetValue(form, out var list)) RemoveFirstNoteWithId(list, id);
        }
        foreach (var part in snapshot.CompoundParts)
        {
            if (_byCompoundPart.TryGetValue(part, out var list)) RemoveFirstNoteWithId(list, id);
        }
        if (_byDerivedFrom.TryGetValue(snapshot.DerivedFrom, out var derivedList))
        {
            RemoveFirstNoteWithId(derivedList, id);
        }
        if (_byDisambiguationName.TryGetValue(snapshot.DisambiguationName, out var disambigList))
        {
            RemoveFirstNoteWithId(disambigList, id);
        }
        foreach (var kanji in snapshot.MainFormKanji)
        {
            if (_byKanjiInMainForm.TryGetValue(kanji, out var list)) RemoveFirstNoteWithId(list, id);
        }
        foreach (var kanji in snapshot.AllKanji)
        {
            if (_byKanjiInAnyForm.TryGetValue(kanji, out var list)) RemoveFirstNoteWithId(list, id);
        }
        foreach (var reading in snapshot.Readings)
        {
            if (_byReading.TryGetValue(reading, out var list)) RemoveFirstNoteWithId(list, id);
        }
        foreach (var stem in snapshot.Stems)
        {
            if (_byStem.TryGetValue(stem, out var list)) RemoveFirstNoteWithId(list, id);
        }
    }

    protected override void InheritorAddToCache(VocabNote note, VocabSnapshot snapshot)
    {
        foreach (var form in snapshot.Forms)
        {
            if (!_byForm.ContainsKey(form)) _byForm[form] = new List<VocabNote>();
            _byForm[form].Add(note);
        }
        foreach (var compoundPart in snapshot.CompoundParts)
        {
            if (!_byCompoundPart.ContainsKey(compoundPart)) _byCompoundPart[compoundPart] = new List<VocabNote>();
            _byCompoundPart[compoundPart].Add(note);
        }
        if (!_byDerivedFrom.ContainsKey(snapshot.DerivedFrom)) _byDerivedFrom[snapshot.DerivedFrom] = new List<VocabNote>();
        _byDerivedFrom[snapshot.DerivedFrom].Add(note);
        
        if (!_byDisambiguationName.ContainsKey(snapshot.DisambiguationName)) _byDisambiguationName[snapshot.DisambiguationName] = new List<VocabNote>();
        _byDisambiguationName[snapshot.DisambiguationName].Add(note);
        
        foreach (var kanji in snapshot.MainFormKanji)
        {
            if (!_byKanjiInMainForm.ContainsKey(kanji)) _byKanjiInMainForm[kanji] = new List<VocabNote>();
            _byKanjiInMainForm[kanji].Add(note);
        }
        foreach (var kanji in snapshot.AllKanji)
        {
            if (!_byKanjiInAnyForm.ContainsKey(kanji)) _byKanjiInAnyForm[kanji] = new List<VocabNote>();
            _byKanjiInAnyForm[kanji].Add(note);
        }
        foreach (var reading in snapshot.Readings)
        {
            if (!_byReading.ContainsKey(reading)) _byReading[reading] = new List<VocabNote>();
            _byReading[reading].Add(note);
        }
        foreach (var stem in snapshot.Stems)
        {
            if (!_byStem.ContainsKey(stem)) _byStem[stem] = new List<VocabNote>();
            _byStem[stem].Add(note);
        }
    }
}
