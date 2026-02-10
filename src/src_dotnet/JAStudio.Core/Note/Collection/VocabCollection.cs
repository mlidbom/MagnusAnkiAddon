using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.Note.Collection;

public class VocabCollection
{
    private readonly IBackendNoteCreator _backendNoteCreator;
    internal readonly VocabCache Cache;
    public IAnkiNoteUpdateHandler AnkiSyncHandler => Cache;

    public VocabCollection(IBackendNoteCreator backendNoteCreator, NoteServices noteServices)
    {
        _backendNoteCreator = backendNoteCreator;
        Cache = new VocabCache(noteServices);
    }

    public bool IsWord(string form) => Cache.WithForm(form).Any();
    public List<VocabNote> All() => Cache.All();
    public VocabNote? WithIdOrNone(NoteId noteId) => Cache.WithIdOrNone(noteId);
    public VocabNote? WithAnkiIdOrNone(long ankiNoteId) => Cache.WithAnkiIdOrNone(ankiNoteId);
    public NoteId? AnkiIdToNoteId(long ankiNoteId) => Cache.AnkiIdToNoteId(ankiNoteId);
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