using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
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
        var fields = new Dictionary<string, string>
        {
            [NoteFieldsConstants.Kanji.Question] = dto.Kanji,
            [NoteFieldsConstants.Kanji.SourceAnswer] = dto.SourceAnswer,
            [NoteFieldsConstants.Kanji.UserAnswer] = dto.UserAnswer,
            [NoteFieldsConstants.Kanji.ActiveAnswer] = dto.ActiveAnswer,
            [NoteFieldsConstants.Kanji.ReadingOn] = dto.ReadingOnHtml,
            [NoteFieldsConstants.Kanji.ReadingKun] = dto.ReadingKunHtml,
            [NoteFieldsConstants.Kanji.ReadingNan] = dto.ReadingNanHtml,
            [NoteFieldsConstants.Kanji.Radicals] = string.Join(", ", dto.Radicals),
            [NoteFieldsConstants.Kanji.SourceMeaningMnemonic] = dto.SourceMeaningMnemonic,
            [NoteFieldsConstants.Kanji.MeaningInfo] = dto.MeaningInfo,
            [NoteFieldsConstants.Kanji.ReadingMnemonic] = dto.ReadingMnemonic,
            [NoteFieldsConstants.Kanji.ReadingInfo] = dto.ReadingInfo,
            [NoteFieldsConstants.Kanji.PrimaryVocab] = string.Join(", ", dto.PrimaryVocab),
            [NoteFieldsConstants.Kanji.Audio] = dto.Audio,
            [NoteFieldsConstants.Kanji.UserMnemonic] = dto.UserMnemonic,
            [NoteFieldsConstants.Kanji.UserSimilarMeaning] = string.Join(", ", dto.SimilarMeaning),
            [NoteFieldsConstants.Kanji.RelatedConfusedWith] = string.Join(", ", dto.ConfusedWith),
            [MyNoteFields.JasNoteId] = dto.Id.ToString(),
        };

        return new NoteData(new KanjiId(dto.Id), fields, dto.Tags.ToList());
    }
}
