using System.Collections.Generic;

namespace JAStudio.Core.Note.CorpusData;

public class SentenceData : CorpusDataBase
{
   public string SourceQuestion { get; init; } = string.Empty;
   public string UserQuestion { get; init; } = string.Empty;
   public string ActiveQuestion { get; init; } = string.Empty;
   public string SourceAnswer { get; init; } = string.Empty;
   public string UserAnswer { get; init; } = string.Empty;
   public string ActiveAnswer { get; init; } = string.Empty;
   public string SourceComments { get; init; } = string.Empty;
   public string UserComments { get; init; } = string.Empty;
   public string Reading { get; init; } = string.Empty;
   public string ExternalId { get; init; } = string.Empty;
   public string Audio { get; init; } = string.Empty;
   public string Screenshot { get; init; } = string.Empty;
   public string Configuration { get; init; } = string.Empty;
   public string ParsingResult { get; init; } = string.Empty;
   public string JanomeTokens { get; init; } = string.Empty;

   public SentenceData(SentenceId id, List<string> tags) : base(id, tags) { }

   protected override void PopulateFields(Dictionary<string, string> fields)
   {
      fields[SentenceNoteFields.SourceQuestion] = SourceQuestion;
      fields[SentenceNoteFields.UserQuestion] = UserQuestion;
      fields[SentenceNoteFields.ActiveQuestion] = ActiveQuestion;
      fields[SentenceNoteFields.SourceAnswer] = SourceAnswer;
      fields[SentenceNoteFields.UserAnswer] = UserAnswer;
      fields[SentenceNoteFields.ActiveAnswer] = ActiveAnswer;
      fields[SentenceNoteFields.SourceComments] = SourceComments;
      fields[SentenceNoteFields.UserComments] = UserComments;
      fields[SentenceNoteFields.Reading] = Reading;
      fields[SentenceNoteFields.Id] = ExternalId;
      fields[SentenceNoteFields.Audio] = Audio;
      fields[SentenceNoteFields.Screenshot] = Screenshot;
      fields[SentenceNoteFields.Configuration] = Configuration;
      fields[SentenceNoteFields.ParsingResult] = ParsingResult;
      fields[SentenceNoteFields.JanomeTokens] = JanomeTokens;
   }

   public static SentenceData FromAnki(Anki.AnkiSentenceNote anki) =>
      new(anki.Id as SentenceId ?? SentenceId.New(), new List<string>(anki.Tags))
      {
         SourceQuestion = anki.SourceQuestion,
         UserQuestion = anki.UserQuestion,
         ActiveQuestion = anki.ActiveQuestion,
         SourceAnswer = anki.SourceAnswer,
         UserAnswer = anki.UserAnswer,
         ActiveAnswer = anki.ActiveAnswer,
         SourceComments = anki.SourceComments,
         UserComments = anki.UserComments,
         Reading = anki.Reading,
         ExternalId = anki.ExternalId,
         Audio = anki.Audio,
         Screenshot = anki.Screenshot,
         Configuration = anki.Configuration,
         ParsingResult = anki.ParsingResult,
         JanomeTokens = anki.JanomeTokens,
      };
}
