using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Sentences.Serialization;
using JAStudio.Core.Storage.Dto;

namespace JAStudio.Core.Storage.Converters;

public static class SentenceNoteConverter
{
    static readonly SentenceConfigurationSerializer ConfigSerializer = SentenceConfigurationSerializer.Instance;
    static readonly ParsingResultSerializer ParsingSerializer = new();

    public static SentenceNoteDto ToDto(SentenceNote note)
    {
        var configJson = note.GetField(SentenceNoteFields.Configuration);
        var config = ConfigSerializer.Deserialize(configJson, () => { });

        var parsingJson = note.GetField(SentenceNoteFields.ParsingResult);
        var parsingResult = ParsingSerializer.Deserialize(parsingJson);

        return new SentenceNoteDto
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
            Configuration = ToConfigurationDto(config),
            ParsingResult = ToParsingResultDto(parsingResult),
            JanomeTokens = note.GetField(SentenceNoteFields.JanomeTokens),
            Tags = note.Tags.ToStringList(),
        };
    }

    public static NoteData FromDto(SentenceNoteDto dto)
    {
        return FromDtoToCorpusData(dto).ToNoteData();
    }

    public static SentenceData FromDtoToCorpusData(SentenceNoteDto dto)
    {
        return new SentenceData(new SentenceId(dto.Id), dto.Tags.ToList())
        {
            SourceQuestion = dto.SourceQuestion,
            UserQuestion = dto.UserQuestion,
            ActiveQuestion = dto.ActiveQuestion,
            SourceAnswer = dto.SourceAnswer,
            UserAnswer = dto.UserAnswer,
            ActiveAnswer = dto.ActiveAnswer,
            SourceComments = dto.SourceComments,
            UserComments = dto.UserComments,
            Reading = dto.Reading,
            ExternalId = dto.ExternalId,
            Audio = dto.Audio,
            Screenshot = dto.Screenshot,
            Configuration = SerializeConfiguration(dto.Configuration),
            ParsingResult = SerializeParsingResult(dto.ParsingResult),
            JanomeTokens = dto.JanomeTokens,
        };
    }

    static SentenceConfigurationDto ToConfigurationDto(SentenceConfiguration config)
    {
        return new SentenceConfigurationDto
        {
            HighlightedWords = config.HighlightedWords.ToList(),
            IncorrectMatches = config.IncorrectMatches.Get().Select(ToWordExclusionDto).ToList(),
            HiddenMatches = config.HiddenMatches.Get().Select(ToWordExclusionDto).ToList(),
        };
    }

    static WordExclusionDto ToWordExclusionDto(WordExclusion exclusion)
    {
        return new WordExclusionDto
        {
            Word = exclusion.Word,
            Index = exclusion.Index,
        };
    }

    static ParsingResultDto? ToParsingResultDto(ParsingResult? result)
    {
        if (result == null || string.IsNullOrEmpty(result.Sentence))
            return null;

        return new ParsingResultDto
        {
            Sentence = result.Sentence,
            ParserVersion = result.ParserVersion,
            ParsedWords = result.ParsedWords.Select(ToMatchDto).ToList(),
        };
    }

    static ParsedMatchDto ToMatchDto(ParsedMatch match)
    {
        return new ParsedMatchDto
        {
            Variant = match.Variant,
            StartIndex = match.StartIndex,
            IsDisplayed = match.IsDisplayed,
            ParsedForm = match.ParsedForm,
            VocabId = match.VocabId?.Value,
        };
    }

    static string SerializeConfiguration(SentenceConfigurationDto dto)
    {
        var config = new SentenceConfiguration(
            dto.HighlightedWords.ToList(),
            new WordExclusionSet(() => { }, dto.IncorrectMatches.Select(FromWordExclusionDto).ToList()),
            new WordExclusionSet(() => { }, dto.HiddenMatches.Select(FromWordExclusionDto).ToList())
        );
        return ConfigSerializer.Serialize(config);
    }

    static WordExclusion FromWordExclusionDto(WordExclusionDto dto)
    {
        return dto.Index == -1
            ? WordExclusion.Global(dto.Word)
            : WordExclusion.AtIndex(dto.Word, dto.Index);
    }

    static string SerializeParsingResult(ParsingResultDto? dto)
    {
        if (dto == null)
            return string.Empty;

        var result = new ParsingResult(
            dto.ParsedWords.Select(FromMatchDto).ToList(),
            dto.Sentence,
            dto.ParserVersion
        );
        return ParsingSerializer.Serialize(result);
    }

    static ParsedMatch FromMatchDto(ParsedMatchDto dto)
    {
        NoteId? vocabId = dto.VocabId.HasValue ? new VocabId(dto.VocabId.Value) : null;

        return new ParsedMatch(
            dto.Variant,
            dto.StartIndex,
            dto.IsDisplayed,
            dto.ParsedForm,
            vocabId
        );
    }
}
