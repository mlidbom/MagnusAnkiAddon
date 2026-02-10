using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Note.Vocabulary.RelatedVocab;
using JAStudio.Core.Storage.Dto;

namespace JAStudio.Core.Storage.Converters;

public static class VocabNoteConverter
{
    static readonly VocabNoteMatchingRulesSerializer MatchingRulesSerializer = new();
    static readonly RelatedVocabDataSerializer RelatedVocabSerializer = RelatedVocabData.Serializer();

    public static VocabNoteDto ToDto(VocabNote note)
    {
        var matchingRulesJson = note.GetField(NoteFieldsConstants.Vocab.MatchingRules);
        var relatedVocabJson = note.GetField(NoteFieldsConstants.Vocab.RelatedVocab);
        var matchingRulesData = MatchingRulesSerializer.Deserialize(matchingRulesJson);
        var relatedVocabData = RelatedVocabSerializer.Deserialize(relatedVocabJson);

        return new VocabNoteDto
        {
            Id = note.GetId().Value,
            Question = note.GetField(NoteFieldsConstants.Vocab.Question),
            SourceAnswer = note.GetField(NoteFieldsConstants.Vocab.SourceAnswer),
            UserAnswer = note.GetField(NoteFieldsConstants.Vocab.UserAnswer),
            ActiveAnswer = note.GetField(NoteFieldsConstants.Vocab.ActiveAnswer),
            UserExplanation = note.GetField(NoteFieldsConstants.Vocab.UserExplanation),
            UserExplanationLong = note.GetField(NoteFieldsConstants.Vocab.UserExplanationLong),
            UserMnemonic = note.GetField(NoteFieldsConstants.Vocab.UserMnemonic),
            UserCompounds = StringExtensions.ExtractCommaSeparatedValues(note.GetField(NoteFieldsConstants.Vocab.UserCompounds)),
            Readings = StringExtensions.ExtractCommaSeparatedValues(note.GetField(NoteFieldsConstants.Vocab.Reading)),
            PartsOfSpeech = note.GetField(NoteFieldsConstants.Vocab.PartsOfSpeech),
            SourceMnemonic = note.GetField(NoteFieldsConstants.Vocab.SourceMnemonic),
            SourceReadingMnemonic = note.GetField(NoteFieldsConstants.Vocab.SourceReadingMnemonic),
            AudioB = note.GetField(NoteFieldsConstants.Vocab.AudioB),
            AudioG = note.GetField(NoteFieldsConstants.Vocab.AudioG),
            AudioTTS = note.GetField(NoteFieldsConstants.Vocab.AudioTTS),
            Forms = StringExtensions.ExtractCommaSeparatedValues(note.GetField(NoteFieldsConstants.Vocab.Forms)),
            SentenceCount = int.TryParse(note.GetField(NoteFieldsConstants.Vocab.SentenceCount), out var sc) ? sc : 0,
            MatchingRules = ToMatchingRulesDto(matchingRulesData),
            RelatedVocab = ToRelatedVocabDto(relatedVocabData),
            Tags = note.Tags.ToStringList(),
        };
    }

    public static NoteData FromDto(VocabNoteDto dto)
    {
        var fields = new Dictionary<string, string>
        {
            [NoteFieldsConstants.Vocab.Question] = dto.Question,
            [NoteFieldsConstants.Vocab.SourceAnswer] = dto.SourceAnswer,
            [NoteFieldsConstants.Vocab.UserAnswer] = dto.UserAnswer,
            [NoteFieldsConstants.Vocab.ActiveAnswer] = dto.ActiveAnswer,
            [NoteFieldsConstants.Vocab.UserExplanation] = dto.UserExplanation,
            [NoteFieldsConstants.Vocab.UserExplanationLong] = dto.UserExplanationLong,
            [NoteFieldsConstants.Vocab.UserMnemonic] = dto.UserMnemonic,
            [NoteFieldsConstants.Vocab.UserCompounds] = string.Join(", ", dto.UserCompounds),
            [NoteFieldsConstants.Vocab.Reading] = string.Join(", ", dto.Readings),
            [NoteFieldsConstants.Vocab.PartsOfSpeech] = dto.PartsOfSpeech,
            [NoteFieldsConstants.Vocab.SourceMnemonic] = dto.SourceMnemonic,
            [NoteFieldsConstants.Vocab.SourceReadingMnemonic] = dto.SourceReadingMnemonic,
            [NoteFieldsConstants.Vocab.AudioB] = dto.AudioB,
            [NoteFieldsConstants.Vocab.AudioG] = dto.AudioG,
            [NoteFieldsConstants.Vocab.AudioTTS] = dto.AudioTTS,
            [NoteFieldsConstants.Vocab.Forms] = string.Join(", ", dto.Forms),
            [NoteFieldsConstants.Vocab.SentenceCount] = dto.SentenceCount.ToString(),
            [NoteFieldsConstants.Vocab.MatchingRules] = MatchingRulesSerializer.Serialize(FromMatchingRulesDto(dto.MatchingRules)),
            [NoteFieldsConstants.Vocab.RelatedVocab] = RelatedVocabSerializer.Serialize(FromRelatedVocabDto(dto.RelatedVocab)),
            [MyNoteFields.JasNoteId] = dto.Id.ToString(),
        };

        return new NoteData(new VocabId(dto.Id), fields, dto.Tags.ToList());
    }

    static VocabMatchingRulesDto ToMatchingRulesDto(VocabNoteMatchingRulesData data)
    {
        return new VocabMatchingRulesDto
        {
            PrefixIsNot = data.PrefixIsNot.ToList(),
            SuffixIsNot = data.SuffixIsNot.ToList(),
            SurfaceIsNot = data.SurfaceIsNot.ToList(),
            YieldToSurface = data.YieldToSurface.ToList(),
            RequiredPrefix = data.RequiredPrefix.ToList(),
        };
    }

    static VocabNoteMatchingRulesData FromMatchingRulesDto(VocabMatchingRulesDto dto)
    {
        return new VocabNoteMatchingRulesData(
            dto.SurfaceIsNot.ToHashSet(),
            dto.PrefixIsNot.ToHashSet(),
            dto.SuffixIsNot.ToHashSet(),
            dto.RequiredPrefix.ToHashSet(),
            dto.YieldToSurface.ToHashSet()
        );
    }

    static VocabRelatedDataDto ToRelatedVocabDto(RelatedVocabData data)
    {
        return new VocabRelatedDataDto
        {
            ErgativeTwin = data.ErgativeTwin,
            DerivedFrom = data.DerivedFrom.Get(),
            PerfectSynonyms = data.PerfectSynonyms.ToList(),
            Synonyms = data.Synonyms.ToList(),
            Antonyms = data.Antonyms.ToList(),
            ConfusedWith = data.ConfusedWith.ToList(),
            SeeAlso = data.SeeAlso.ToList(),
        };
    }

    static RelatedVocabData FromRelatedVocabDto(VocabRelatedDataDto dto)
    {
        return new RelatedVocabData(
            dto.ErgativeTwin,
            new Note.NoteFields.AutoSaveWrappers.ValueWrapper<string>(dto.DerivedFrom),
            dto.PerfectSynonyms.ToHashSet(),
            dto.Synonyms.ToHashSet(),
            dto.Antonyms.ToHashSet(),
            dto.ConfusedWith.ToHashSet(),
            dto.SeeAlso.ToHashSet()
        );
    }
}
