using System;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.Sentences.Serialization;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Sentences;

public class CachingSentenceConfigurationField
{
    private readonly SentenceNote _sentence;
    private readonly NoteGuard _guard;
    private SentenceConfiguration _value;

    public CachingSentenceConfigurationField(SentenceNote sentence, SentenceConfigSubData? data, NoteGuard guard)
    {
        _sentence = sentence;
        _guard = guard;
        _value = SentenceData.CreateConfiguration(data, OnMutated);
    }

    public SentenceConfiguration Configuration => _value;

    public WordExclusionSet IncorrectMatches => _value.IncorrectMatches;

    public WordExclusionSet HiddenMatches => _value.HiddenMatches;

    public List<string> HighlightedWords => _value.HighlightedWords;

    public HashSet<VocabNote> HighlightedVocab()
    {
        var highlightedWordsList = HighlightedWords.ToList();
        var vocabWithForms = _sentence.Services.Collection.Vocab.WithAnyFormIn(highlightedWordsList);
        var matchedVocabIds = _sentence.GetParsingResult().MatchedVocabIds;
        
        return vocabWithForms
            .Where(vocab => matchedVocabIds.Contains(vocab.GetId()))
            .ToHashSet();
    }

    public void RemoveHighlightedWord(string word)
    {
        HighlightedWords.Remove(word);
        OnMutated();
    }

    public void ResetHighlightedWords()
    {
        _value.HighlightedWords.Clear();
        OnMutated();
    }

    public void AddHighlightedWord(string vocab)
    {
        HighlightedWords.Add(vocab.Trim());
        OnMutated();
    }

    void OnMutated()
    {
        _guard.MarkDirty();
        _sentence.UpdateParsedWords(force: true);
    }

    [Obsolete("For testing only")]
    public void SetValueDirectlyTestsOnly(SentenceConfiguration configuration)
    {
        _value = configuration;
    }
}
