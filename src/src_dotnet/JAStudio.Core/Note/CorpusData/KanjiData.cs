using System.Collections.Generic;

namespace JAStudio.Core.Note.CorpusData;

public class KanjiData : CorpusDataBase
{
   public string Question { get; init; } = string.Empty;
   public string SourceAnswer { get; init; } = string.Empty;
   public string UserAnswer { get; init; } = string.Empty;
   public string ActiveAnswer { get; init; } = string.Empty;
   public string ReadingOn { get; init; } = string.Empty;
   public string ReadingKun { get; init; } = string.Empty;
   public string ReadingNan { get; init; } = string.Empty;
   public string Radicals { get; init; } = string.Empty;
   public string SourceMeaningMnemonic { get; init; } = string.Empty;
   public string MeaningInfo { get; init; } = string.Empty;
   public string ReadingMnemonic { get; init; } = string.Empty;
   public string ReadingInfo { get; init; } = string.Empty;
   public string PrimaryVocab { get; init; } = string.Empty;
   public string Audio { get; init; } = string.Empty;
   public string UserMnemonic { get; init; } = string.Empty;
   public string UserSimilarMeaning { get; init; } = string.Empty;
   public string RelatedConfusedWith { get; init; } = string.Empty;
   public string Image { get; init; } = string.Empty;

   public KanjiData(KanjiId id, List<string> tags) : base(id, tags) { }

   protected override void PopulateFields(Dictionary<string, string> fields)
   {
      fields[NoteFieldsConstants.Kanji.Question] = Question;
      fields[NoteFieldsConstants.Kanji.SourceAnswer] = SourceAnswer;
      fields[NoteFieldsConstants.Kanji.UserAnswer] = UserAnswer;
      fields[NoteFieldsConstants.Kanji.ActiveAnswer] = ActiveAnswer;
      fields[NoteFieldsConstants.Kanji.ReadingOn] = ReadingOn;
      fields[NoteFieldsConstants.Kanji.ReadingKun] = ReadingKun;
      fields[NoteFieldsConstants.Kanji.ReadingNan] = ReadingNan;
      fields[NoteFieldsConstants.Kanji.Radicals] = Radicals;
      fields[NoteFieldsConstants.Kanji.SourceMeaningMnemonic] = SourceMeaningMnemonic;
      fields[NoteFieldsConstants.Kanji.MeaningInfo] = MeaningInfo;
      fields[NoteFieldsConstants.Kanji.ReadingMnemonic] = ReadingMnemonic;
      fields[NoteFieldsConstants.Kanji.ReadingInfo] = ReadingInfo;
      fields[NoteFieldsConstants.Kanji.PrimaryVocab] = PrimaryVocab;
      fields[NoteFieldsConstants.Kanji.Audio] = Audio;
      fields[NoteFieldsConstants.Kanji.UserMnemonic] = UserMnemonic;
      fields[NoteFieldsConstants.Kanji.UserSimilarMeaning] = UserSimilarMeaning;
      fields[NoteFieldsConstants.Kanji.RelatedConfusedWith] = RelatedConfusedWith;
   }

   public static KanjiData FromAnki(Anki.AnkiKanjiNote anki) =>
      new(anki.Id as KanjiId ?? KanjiId.New(), new List<string>(anki.Tags))
      {
         Question = anki.Question,
         SourceAnswer = anki.SourceAnswer,
         UserAnswer = anki.UserAnswer,
         ActiveAnswer = anki.ActiveAnswer,
         ReadingOn = anki.ReadingOn,
         ReadingKun = anki.ReadingKun,
         ReadingNan = anki.ReadingNan,
         Radicals = anki.Radicals,
         SourceMeaningMnemonic = anki.SourceMeaningMnemonic,
         MeaningInfo = anki.MeaningInfo,
         ReadingMnemonic = anki.ReadingMnemonic,
         ReadingInfo = anki.ReadingInfo,
         PrimaryVocab = anki.PrimaryVocab,
         Audio = anki.Audio,
         UserMnemonic = anki.UserMnemonic,
         UserSimilarMeaning = anki.UserSimilarMeaning,
         RelatedConfusedWith = anki.RelatedConfusedWith,
         Image = anki.Image,
      };
}
