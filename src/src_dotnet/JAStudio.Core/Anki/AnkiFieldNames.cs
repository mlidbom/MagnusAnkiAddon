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
      public const string MatchingRules = "__matching_rules"; //Remove
      public const string RelatedVocab = "__related_vocab"; //Remove
      public const string SentenceCount = "sentence_count"; //Remove
      public const string Question = AnkiFieldNames.Question; //Sync only to anki, not from
      public const string ActiveAnswer = AnkiFieldNames.Answer; //Sync only to anki, not from
      public const string SourceAnswer = "source_answer"; //Remove
      public const string UserAnswer = "__answer"; //Remove
      public const string UserExplanation = "__explanation"; //Remove
      public const string UserExplanationLong = "__explanation_long"; //Remove
      public const string UserCompounds = "__compounds"; //Remove
      public const string UserMnemonic = "__mnemonic"; //Remove
      public const string Reading = "Reading"; //Remove
      public const string PartsOfSpeech = "TOS"; //Remove
      public const string SourceMnemonic = "source_mnemonic"; //Remove
      public const string AudioB = "Audio_b"; //Sync only to anki, not from
      public const string AudioG = "Audio_g"; //Sync only to anki, not from
      public const string AudioTTS = "Audio_TTS"; //Sync only to anki, not from
      public const string Kanji = "__kanji"; //Remove
      public const string Forms = "F"; //Remove
      public const string SourceReadingMnemonic = "source_reading_mnemonic"; //Remove
      public const string TechnicalNotes = "__technical_notes"; //Not imported into our store yet. Once we have it can be removed.
      public const string Image = "Image";  //Remove
      public const string UserImage = "__image"; //Remove
   }

   public static class Kanji
   {
      public const string Question = AnkiFieldNames.Question; //Sync only to anki, not from
      public const string ActiveAnswer = AnkiFieldNames.Answer; //Sync only to anki, not from
      public const string SourceAnswer = "source_answer";
      public const string UserAnswer = "__answer"; //Remove
      public const string ReadingOn = "Reading_On"; //Remove
      public const string ReadingKun = "Reading_Kun"; //Remove
      public const string ReadingNan = "__reading_Nan"; //Remove
      public const string Radicals = "Radicals"; //Remove
      public const string SourceMeaningMnemonic = "Meaning_Mnemonic"; //Remove
      public const string MeaningInfo = "Meaning_Info"; //Remove
      public const string ReadingMnemonic = "Reading_Mnemonic"; //Remove
      public const string ReadingInfo = "Reading_Info"; //Remove
      public const string PrimaryVocab = "__primary_Vocab"; //Remove
      public const string Audio = "__audio";
      public const string UserMnemonic = "__mnemonic"; //Remove
      public const string UserSimilarMeaning = "__similar_meaning"; //Remove
      public const string RelatedConfusedWith = "__confused_with"; //Remove
      public const string Image = "_image"; //Remove
   }

   public static class Sentence
   {
      public const string Reading = "Reading"; //Remove
      public const string Id = "ID"; //Read only on first import, then can be ignored, We may want to importd directly from other note types and not have this at all
      public const string ActiveQuestion = AnkiFieldNames.Question; //Remove
      public const string SourceQuestion = "source_question"; //Read only on first import, then can be ignored, We may want to importd directly from other note types and not have this at all
      public const string SourceComments = "Comments"; //Read only on first import, then can be ignored
      public const string UserComments = "__comments"; //Remove
      public const string UserQuestion = "__question"; //Remove
      public const string ActiveAnswer = AnkiFieldNames.Answer; //Remove
      public const string SourceAnswer = "source_answer"; //Read only on first import, then can be ignored, We may want to importd directly from other note types and not have this at all
      public const string UserAnswer = "__answer"; //Remove
      public const string ParsingResult = "__parsing_result"; //Remove
      public const string JanomeTokens = "__janome_tokens"; //Remove
      public const string Audio = "Audio Sentence"; //Read only on first import, then sync only to anki
      public const string Screenshot = "Screenshot"; //Read only on first import, then sync only to anki
      public const string Configuration = "__configuration"; //Remove
   }

   public static class ImmersionKit
   {
      public const string Audio = "Audio Sentence"; //Read only once to do conversion to our sentence type
      public const string Id = "ID";//Read only once to do conversion to our sentence type
      public const string Screenshot = "Screenshot";//Read only once to do conversion to our sentence type
      public const string Reading = "Reading";//Read only once to do conversion to our sentence type
      public const string Answer = "English";//Read only once to do conversion to our sentence type
      public const string Question = "Expression";//Read only once to do conversion to our sentence type
   }
}
