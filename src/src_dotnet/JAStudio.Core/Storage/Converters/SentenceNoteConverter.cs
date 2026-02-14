using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Sentences.Serialization;

namespace JAStudio.Core.Storage.Converters;

public static class SentenceNoteConverter
{
    static readonly SentenceConfigurationSerializer ConfigSerializer = SentenceConfigurationSerializer.Instance;
    static readonly ParsingResultSerializer ParsingSerializer = new();

    public static SentenceData ToCorpusData(SentenceNote note)
    {
        var configJson = note.GetField(SentenceNoteFields.Configuration);
        var config = ConfigSerializer.Deserialize(configJson, () => { });

        var parsingJson = note.GetField(SentenceNoteFields.ParsingResult);
        var parsingResult = ParsingSerializer.Deserialize(parsingJson);

        return new SentenceData
        {
            Id = note.GetId().Value,
            SourceQuestion = note.GetField(SentenceNoteFields.SourceQuestion),
            UserQuestion = note.GetField(SentenceNoteFields.UserQuestion),
            ActiveQuestion = note.GetField(SentenceNoteFields.ActiveQuestion),
            SourceAnswer = note.GetField(SentenceNoteFields.SourceAnswer),
            UserAnswer = note.GetField(SentenceNoteFields.UserAnswer),
            ActiveAnswer = note.GetField(SentenceNoteFields.ActiveAnswer),
            SourceComments = note.GetField(SentenceNoteFields.SourceComments),
            UserComments = note.GetField(SentenceNoteFields.UserComments),
            Reading = note.GetField(SentenceNoteFields.Reading),
            ExternalId = note.GetField(SentenceNoteFields.Id),
            Audio = note.GetField(SentenceNoteFields.Audio),
            Screenshot = note.GetField(SentenceNoteFields.Screenshot),
            Configuration = ToConfigSubData(config),
            ParsingResult = ToParsingResultSubData(parsingResult),
            JanomeTokens = note.GetField(SentenceNoteFields.JanomeTokens),
            Tags = note.Tags.ToStringList(),
        };
    }

    static SentenceConfigSubData ToConfigSubData(SentenceConfiguration config)
    {
        return new SentenceConfigSubData
        {
            HighlightedWords = config.HighlightedWords.ToList(),
            IncorrectMatches = config.IncorrectMatches.Get().Select(ToWordExclusionSubData).ToList(),
            HiddenMatches = config.HiddenMatches.Get().Select(ToWordExclusionSubData).ToList(),
        };
    }

    static WordExclusionSubData ToWordExclusionSubData(WordExclusion exclusion)
    {
        return new WordExclusionSubData
        {
            Word = exclusion.Word,
            Index = exclusion.Index,
        };
    }

    static SentenceParsingResultSubData? ToParsingResultSubData(ParsingResult? result)
    {
        if (result == null || string.IsNullOrEmpty(result.Sentence))
            return null;

        return new SentenceParsingResultSubData
        {
            Sentence = result.Sentence,
            ParserVersion = result.ParserVersion,
            ParsedWords = result.ParsedWords.Select(ToMatchSubData).ToList(),
        };
    }

    static ParsedMatchSubData ToMatchSubData(ParsedMatch match)
    {
        return new ParsedMatchSubData
        {
            Variant = match.Variant,
            StartIndex = match.StartIndex,
            IsDisplayed = match.IsDisplayed,
            ParsedForm = match.ParsedForm,
            VocabId = match.VocabId?.Value,
        };
    }
}
