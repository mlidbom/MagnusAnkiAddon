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
            SourceAnswer = note.SourceAnswer.Value,
            UserAnswer = note.UserAnswer.Value,
            ActiveAnswer = note.ActiveAnswer.Value,
            ReadingOnHtml = note.ReadingOnHtml.Value,
            ReadingKunHtml = note.ReadingKunHtml.Value,
            ReadingNanHtml = note.ReadingNanHtml.Value,
            Radicals = note.AllRadicals,
            SourceMeaningMnemonic = note.SourceMeaningMnemonic.Value,
            MeaningInfo = note.MeaningInfo.Value,
            ReadingMnemonic = note.ReadingMnemonic.Value,
            ReadingInfo = note.ReadingInfo.Value,
            PrimaryVocab = note.PrimaryVocab,
            Audio = note.Audio.RawValue(),
            PrimaryReadingsTtsAudio = note.PrimaryReadingsTtsAudio.Value,
            References = note.KanjiReferences.Value,
            UserMnemonic = note.UserMnemonic.Value,
            SimilarMeaning = note.UserSimilarMeaning,
            ConfusedWith = note.RelatedConfusedWith,
            Image = note.Image.RawValue(),
            Tags = note.Tags.ToStringList(),
        };
    }
}
