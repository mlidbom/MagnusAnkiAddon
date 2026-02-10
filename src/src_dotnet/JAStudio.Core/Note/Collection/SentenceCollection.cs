using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Collection;

public class SentenceCollection
{
    private readonly IBackendNoteCreator _backendNoteCreator;
    internal readonly SentenceCache Cache;
    public IAnkiNoteUpdateHandler AnkiSyncHandler => Cache;

    public SentenceCollection(IBackendNoteCreator backendNoteCreator, NoteServices noteServices)
    {
        _backendNoteCreator = backendNoteCreator;
        Cache = new SentenceCache(noteServices);
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

    public SentenceNote? WithIdOrNone(NoteId noteId) => Cache.WithIdOrNone(noteId);
    public SentenceNote? WithAnkiIdOrNone(long ankiNoteId) => Cache.WithAnkiIdOrNone(ankiNoteId);
    public NoteId? AnkiIdToNoteId(long ankiNoteId) => Cache.AnkiIdToNoteId(ankiNoteId);

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