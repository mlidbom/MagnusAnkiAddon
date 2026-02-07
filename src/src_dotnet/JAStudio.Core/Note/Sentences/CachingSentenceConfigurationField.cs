using System;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Sentences.Serialization;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Sentences;

public class CachingSentenceConfigurationField
{
    private readonly SentenceNote _sentence;
    public readonly MutableStringField Field;
    private SentenceConfiguration _value;

    public CachingSentenceConfigurationField(SentenceNote sentence)
    {
        _sentence = sentence;
        Field = new MutableStringField(sentence, SentenceNoteFields.Configuration);
        _value = SentenceConfigurationSerializer.Instance.Deserialize(Field.Value, Save);
    }

    public SentenceConfiguration Configuration => _value;

    public WordExclusionSet IncorrectMatches => _value.IncorrectMatches;

    public WordExclusionSet HiddenMatches => _value.HiddenMatches;

    public List<string> HighlightedWords => _value.HighlightedWords;

    public HashSet<VocabNote> HighlightedVocab()
    {
        var highlightedWordsList = HighlightedWords.ToList();
        var vocabWithForms = _sentence.Services.Collection.Vocab.WithAnyFormIn(highlightedWordsList);
        var matchedVocabIds = _sentence.ParsingResult.Get().MatchedVocabIds;
        
        return vocabWithForms
            .Where(vocab => matchedVocabIds.Contains(vocab.GetId()))
            .ToHashSet();
    }

    public void RemoveHighlightedWord(string word)
    {
        HighlightedWords.Remove(word);
        Save();
    }

    public void ResetHighlightedWords()
    {
        _value.HighlightedWords.Clear();
        Save();
    }

    public void AddHighlightedWord(string vocab)
    {
        HighlightedWords.Add(vocab.Trim());
        Save();
    }

    private void Save()
    {
        Field.Set(SentenceConfigurationSerializer.Instance.Serialize(_value));
        _sentence.UpdateParsedWords(force: true);
    }

    [Obsolete("For testing only")]
    public void SetValueDirectlyTestsOnly(SentenceConfiguration configuration)//TODO: Review
    {
        _value = configuration;
    }
}
