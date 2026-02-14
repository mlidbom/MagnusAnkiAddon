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
            Kanji = note.GetQuestion(),
            SourceAnswer = note.SourceAnswer,
            UserAnswer = note.UserAnswer,
            ActiveAnswer = note.ActiveAnswer,
            ReadingOnHtml = note.ReadingOnHtml,
            ReadingKunHtml = note.ReadingKunHtml,
            ReadingNanHtml = note.ReadingNanHtml,
            Radicals = note.AllRadicals,
            SourceMeaningMnemonic = note.SourceMeaningMnemonic,
            MeaningInfo = note.MeaningInfo,
            ReadingMnemonic = note.ReadingMnemonic,
            ReadingInfo = note.ReadingInfo,
            PrimaryVocab = note.PrimaryVocab,
            Audio = note.Audio.RawValue(),
            PrimaryReadingsTtsAudio = note.GetField(NoteFieldsConstants.Kanji.PrimaryReadingsTtsAudio),
            References = note.GetField(NoteFieldsConstants.Kanji.References),
            UserMnemonic = note.UserMnemonic,
            SimilarMeaning = note.UserSimilarMeaning,
            ConfusedWith = note.RelatedConfusedWith,
            Tags = note.Tags.ToStringList(),
        };
    }
}
