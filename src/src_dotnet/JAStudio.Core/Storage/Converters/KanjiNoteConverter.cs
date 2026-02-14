using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Note.CorpusData;

namespace JAStudio.Core.Storage.Converters;

public static class KanjiNoteConverter
{
    public static KanjiData ToCorpusData(KanjiNote note)
    {
        return new KanjiData
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
}
