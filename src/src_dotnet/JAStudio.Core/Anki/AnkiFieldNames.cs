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
      public const string Question = AnkiFieldNames.Question; //Sync only to anki, not from
      public const string ActiveAnswer = AnkiFieldNames.Answer; //Sync only to anki, not from
      public const string AudioB = "Audio_b"; //Sync only to anki, not from
      public const string AudioG = "Audio_g"; //Sync only to anki, not from
      public const string AudioTTS = "Audio_TTS"; //Sync only to anki, not from
      public const string Image = "Image";
      public const string UserImage = "__image";

      // Kept for QueryBuilder Anki search queries until the Anki fields are actually removed
      public const string Reading = "Reading";
      public const string Forms = "F";
   }

   public static class Kanji
   {
      public const string Question = AnkiFieldNames.Question; //Sync only to anki, not from
      public const string ActiveAnswer = AnkiFieldNames.Answer; //Sync only to anki, not from
      public const string SourceAnswer = "source_answer"; //Sync only to anki, not from
      public const string Audio = "__audio";
      public const string PrimaryReadingsTtsAudio = "_primary_readings_tts_audio"; //Sync from anki (TTS addon writes here)
      public const string Image = "_image";

      // Kept for QueryBuilder Anki search queries until the Anki fields are actually removed
      public const string ReadingOn = "Reading_On";
      public const string ReadingKun = "Reading_Kun";
   }

   public static class Sentence
   {
      public const string Reading = "Reading"; //Read only on first import, then sync only to anki
      public const string Id = "ID"; //Read only on first import, then can be ignored
      public const string SourceQuestion = "source_question"; //Read only on first import, then can be ignored
      public const string SourceComments = "Comments"; //Read only on first import, then can be ignored
      public const string SourceAnswer = "source_answer"; //Read only on first import, then can be ignored
      public const string Audio = "Audio Sentence"; //Read only on first import, then sync only to anki
      public const string Screenshot = "Screenshot"; //Read only on first import, then sync only to anki

      // Kept for QueryBuilder Anki search queries until the Anki field is actually removed
      public const string ParsingResult = "__parsing_result";
   }

   //Do not remove, we will be restoring the ImmersionKit import functionality
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
