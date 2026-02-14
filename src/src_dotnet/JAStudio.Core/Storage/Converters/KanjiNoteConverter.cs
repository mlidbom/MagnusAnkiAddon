using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Storage.Dto;

namespace JAStudio.Core.Storage.Converters;

public static class KanjiNoteConverter
{
    public static KanjiNoteDto ToDto(KanjiNote note)
    {
        return new KanjiNoteDto
        {
            Id = note.GetId().Value,
            Kanji = note.GetField(NoteFieldsConstants.Kanji.Question),
            SourceAnswer = note.GetField(NoteFieldsConstants.Kanji.SourceAnswer),
            UserAnswer = note.GetField(NoteFieldsConstants.Kanji.UserAnswer),
            ActiveAnswer = note.GetField(NoteFieldsConstants.Kanji.ActiveAnswer),
            ReadingOnHtml = note.GetField(NoteFieldsConstants.Kanji.ReadingOn),
            ReadingKunHtml = note.GetField(NoteFieldsConstants.Kanji.ReadingKun),
            ReadingNanHtml = note.GetField(NoteFieldsConstants.Kanji.ReadingNan),
            Radicals = StringExtensions.ExtractCommaSeparatedValues(note.GetField(NoteFieldsConstants.Kanji.Radicals)),
            SourceMeaningMnemonic = note.GetField(NoteFieldsConstants.Kanji.SourceMeaningMnemonic),
            MeaningInfo = note.GetField(NoteFieldsConstants.Kanji.MeaningInfo),
            ReadingMnemonic = note.GetField(NoteFieldsConstants.Kanji.ReadingMnemonic),
            ReadingInfo = note.GetField(NoteFieldsConstants.Kanji.ReadingInfo),
            PrimaryVocab = StringExtensions.ExtractCommaSeparatedValues(note.GetField(NoteFieldsConstants.Kanji.PrimaryVocab)),
            Audio = note.GetField(NoteFieldsConstants.Kanji.Audio),
            UserMnemonic = note.GetField(NoteFieldsConstants.Kanji.UserMnemonic),
            SimilarMeaning = StringExtensions.ExtractCommaSeparatedValues(note.GetField(NoteFieldsConstants.Kanji.UserSimilarMeaning)),
            ConfusedWith = StringExtensions.ExtractCommaSeparatedValues(note.GetField(NoteFieldsConstants.Kanji.RelatedConfusedWith)),
            Tags = note.Tags.ToStringList(),
        };
    }

    public static NoteData FromDto(KanjiNoteDto dto)
    {
        return FromDtoToCorpusData(dto).ToNoteData();
    }

    public static KanjiData FromDtoToCorpusData(KanjiNoteDto dto)
    {
        return new KanjiData(new KanjiId(dto.Id), dto.Tags.ToList())
        {
            Question = dto.Kanji,
            SourceAnswer = dto.SourceAnswer,
            UserAnswer = dto.UserAnswer,
            ActiveAnswer = dto.ActiveAnswer,
            ReadingOn = dto.ReadingOnHtml,
            ReadingKun = dto.ReadingKunHtml,
            ReadingNan = dto.ReadingNanHtml,
            Radicals = string.Join(", ", dto.Radicals),
            SourceMeaningMnemonic = dto.SourceMeaningMnemonic,
            MeaningInfo = dto.MeaningInfo,
            ReadingMnemonic = dto.ReadingMnemonic,
            ReadingInfo = dto.ReadingInfo,
            PrimaryVocab = string.Join(", ", dto.PrimaryVocab),
            Audio = dto.Audio,
            UserMnemonic = dto.UserMnemonic,
            UserSimilarMeaning = string.Join(", ", dto.SimilarMeaning),
            RelatedConfusedWith = string.Join(", ", dto.ConfusedWith),
        };
    }
}
