namespace JAStudio.Core.Anki;

/// Field names as they exist in Anki's note type definitions.
/// Used ONLY by Anki integration code (bulk loader, query builder, Anki note wrappers).
/// Domain code must NOT reference these — use NoteFieldsConstants / SentenceNoteFields instead.
public static class AnkiFieldNames
{
   public const string Question = "Q";
   public const string Answer = "A";
   public const string JasNoteId = "jas_note_id";
   public const string NoteId = "nid";

   public static class VocabCard
   {
      public const string Reading = "Reading";
      public const string Listening = "Listening";
   }

   public static class SentenceCard
   {
      public const string Reading = "Reading";
      public const string Listening = "Listening";
   }

   public static class Vocab
   {
      public const string MatchingRules = "__matching_rules";
      public const string RelatedVocab = "__related_vocab";
      public const string SentenceCount = "sentence_count";
      public const string Question = AnkiFieldNames.Question;
      public const string ActiveAnswer = AnkiFieldNames.Answer;
      public const string SourceAnswer = "source_answer";
      public const string UserAnswer = "__answer";
      public const string UserExplanation = "__explanation";
      public const string UserExplanationLong = "__explanation_long";
      public const string UserCompounds = "__compounds";
      public const string UserMnemonic = "__mnemonic";
      public const string Reading = "Reading";
      public const string PartsOfSpeech = "TOS";
      public const string SourceMnemonic = "source_mnemonic";
      public const string AudioB = "Audio_b";
      public const string AudioG = "Audio_g";
      public const string AudioTTS = "Audio_TTS";
      public const string Kanji = "__kanji";
      public const string Forms = "F";
      public const string SourceReadingMnemonic = "source_reading_mnemonic";
      public const string TechnicalNotes = "__technical_notes";
      public const string Image = "Image";
      public const string UserImage = "__image";
   }

   public static class Kanji
   {
      public const string Question = AnkiFieldNames.Question;
      public const string ActiveAnswer = AnkiFieldNames.Answer;
      public const string SourceAnswer = "source_answer";
      public const string UserAnswer = "__answer";
      public const string ReadingOn = "Reading_On";
      public const string ReadingKun = "Reading_Kun";
      public const string ReadingNan = "__reading_Nan";
      public const string Radicals = "Radicals";
      public const string SourceMeaningMnemonic = "Meaning_Mnemonic";
      public const string MeaningInfo = "Meaning_Info";
      public const string ReadingMnemonic = "Reading_Mnemonic";
      public const string ReadingInfo = "Reading_Info";
      public const string PrimaryVocab = "__primary_Vocab";
      public const string Audio = "__audio";
      public const string UserMnemonic = "__mnemonic";
      public const string UserSimilarMeaning = "__similar_meaning";
      public const string RelatedConfusedWith = "__confused_with";
      public const string Image = "_image";
   }

   public static class Sentence
   {
      public const string Reading = "Reading";
      public const string Id = "ID";
      public const string ActiveQuestion = AnkiFieldNames.Question;
      public const string SourceQuestion = "source_question";
      public const string SourceComments = "Comments";
      public const string UserComments = "__comments";
      public const string UserQuestion = "__question";
      public const string ActiveAnswer = AnkiFieldNames.Answer;
      public const string SourceAnswer = "source_answer";
      public const string UserAnswer = "__answer";
      public const string ParsingResult = "__parsing_result";
      public const string JanomeTokens = "__janome_tokens";
      public const string Audio = "Audio Sentence";
      public const string Screenshot = "Screenshot";
      public const string Configuration = "__configuration";
   }

   public static class ImmersionKit
   {
      public const string Audio = "Audio Sentence";
      public const string Id = "ID";
      public const string Screenshot = "Screenshot";
      public const string Reading = "Reading";
      public const string Answer = "English";
      public const string Question = "Expression";
   }
}
