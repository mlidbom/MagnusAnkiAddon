using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.CorpusData;

public class VocabData : CorpusDataBase
{
   public string Question { get; init; } = string.Empty;
   public string SourceAnswer { get; init; } = string.Empty;
   public string UserAnswer { get; init; } = string.Empty;
   public string ActiveAnswer { get; init; } = string.Empty;
   public string UserExplanation { get; init; } = string.Empty;
   public string UserExplanationLong { get; init; } = string.Empty;
   public string UserMnemonic { get; init; } = string.Empty;
   public string UserCompounds { get; init; } = string.Empty;
   public string Reading { get; init; } = string.Empty;
   public string PartsOfSpeech { get; init; } = string.Empty;
   public string SourceMnemonic { get; init; } = string.Empty;
   public string SourceReadingMnemonic { get; init; } = string.Empty;
   public string AudioB { get; init; } = string.Empty;
   public string AudioG { get; init; } = string.Empty;
   public string AudioTTS { get; init; } = string.Empty;
   public string Forms { get; init; } = string.Empty;
   public string SentenceCount { get; init; } = string.Empty;
   public string MatchingRules { get; init; } = string.Empty;
   public string RelatedVocab { get; init; } = string.Empty;
   public string TechnicalNotes { get; init; } = string.Empty;
   public string Image { get; init; } = string.Empty;
   public string UserImage { get; init; } = string.Empty;

   public VocabData(VocabId id, List<string> tags) : base(id, tags) { }

   protected override void PopulateFields(Dictionary<string, string> fields)
   {
      fields[NoteFieldsConstants.Vocab.Question] = Question;
      fields[NoteFieldsConstants.Vocab.SourceAnswer] = SourceAnswer;
      fields[NoteFieldsConstants.Vocab.UserAnswer] = UserAnswer;
      fields[NoteFieldsConstants.Vocab.ActiveAnswer] = ActiveAnswer;
      fields[NoteFieldsConstants.Vocab.UserExplanation] = UserExplanation;
      fields[NoteFieldsConstants.Vocab.UserExplanationLong] = UserExplanationLong;
      fields[NoteFieldsConstants.Vocab.UserMnemonic] = UserMnemonic;
      fields[NoteFieldsConstants.Vocab.UserCompounds] = UserCompounds;
      fields[NoteFieldsConstants.Vocab.Reading] = Reading;
      fields[NoteFieldsConstants.Vocab.PartsOfSpeech] = PartsOfSpeech;
      fields[NoteFieldsConstants.Vocab.SourceMnemonic] = SourceMnemonic;
      fields[NoteFieldsConstants.Vocab.SourceReadingMnemonic] = SourceReadingMnemonic;
      fields[NoteFieldsConstants.Vocab.AudioB] = AudioB;
      fields[NoteFieldsConstants.Vocab.AudioG] = AudioG;
      fields[NoteFieldsConstants.Vocab.AudioTTS] = AudioTTS;
      fields[NoteFieldsConstants.Vocab.Forms] = Forms;
      fields[NoteFieldsConstants.Vocab.SentenceCount] = SentenceCount;
      fields[NoteFieldsConstants.Vocab.MatchingRules] = MatchingRules;
      fields[NoteFieldsConstants.Vocab.RelatedVocab] = RelatedVocab;
      fields[NoteFieldsConstants.Vocab.TechnicalNotes] = TechnicalNotes;
      fields[NoteFieldsConstants.Vocab.Image] = Image;
      fields[NoteFieldsConstants.Vocab.UserImage] = UserImage;
   }

   /// Creates VocabData from an AnkiVocabNote, mapping Anki field names to corpus properties.
   public static VocabData FromAnki(Anki.AnkiVocabNote anki) =>
      new(anki.Id as VocabId ?? VocabId.New(), new List<string>(anki.Tags))
      {
         Question = anki.Question,
         SourceAnswer = anki.SourceAnswer,
         UserAnswer = anki.UserAnswer,
         ActiveAnswer = anki.ActiveAnswer,
         UserExplanation = anki.UserExplanation,
         UserExplanationLong = anki.UserExplanationLong,
         UserMnemonic = anki.UserMnemonic,
         UserCompounds = anki.UserCompounds,
         Reading = anki.Reading,
         PartsOfSpeech = anki.PartsOfSpeech,
         SourceMnemonic = anki.SourceMnemonic,
         SourceReadingMnemonic = anki.SourceReadingMnemonic,
         AudioB = anki.AudioB,
         AudioG = anki.AudioG,
         AudioTTS = anki.AudioTTS,
         Forms = anki.Forms,
         SentenceCount = anki.SentenceCount,
         MatchingRules = anki.MatchingRules,
         RelatedVocab = anki.RelatedVocab,
         TechnicalNotes = anki.TechnicalNotes,
         Image = anki.Image,
         UserImage = anki.UserImage,
      };
}
