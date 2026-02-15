using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Anki;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Sentences.Serialization;
using MemoryPack;

namespace JAStudio.Core.Note.CorpusData;

[MemoryPackable]
public partial class SentenceData : CorpusDataBase
{
   static readonly SentenceConfigurationSerializer ConfigSerializer = SentenceConfigurationSerializer.Instance;
   static readonly ParsingResultSerializer ParsingSerializer = new();

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
   public SentenceConfigSubData Configuration { get; init; } = new();
   public SentenceParsingResultSubData? ParsingResult { get; init; }
   public string JanomeTokens { get; init; } = string.Empty;

   protected override NoteId CreateTypedId() => new SentenceId(Id);

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
      fields[SentenceNoteFields.Configuration] = SerializeConfiguration();
      fields[SentenceNoteFields.ParsingResult] = SerializeParsingResult();
      fields[SentenceNoteFields.JanomeTokens] = JanomeTokens;
   }

   string SerializeConfiguration()
   {
      var config = new SentenceConfiguration(
         Configuration.HighlightedWords.ToList(),
         new WordExclusionSet(() => {}, Configuration.IncorrectMatches.Select(FromExclusionSubData).ToList()),
         new WordExclusionSet(() => {}, Configuration.HiddenMatches.Select(FromExclusionSubData).ToList()));
      return ConfigSerializer.Serialize(config);
   }

   string SerializeParsingResult()
   {
      if(ParsingResult == null) return string.Empty;

      var result = new ParsingResult(
         ParsingResult.ParsedWords.Select(FromParsedMatchSubData).ToList(),
         ParsingResult.Sentence,
         ParsingResult.ParserVersion);
      return ParsingSerializer.Serialize(result);
   }

   static WordExclusion FromExclusionSubData(WordExclusionSubData d) =>
      d.Index == -1 ? WordExclusion.Global(d.Word) : WordExclusion.AtIndex(d.Word, d.Index);

   static ParsedMatch FromParsedMatchSubData(ParsedMatchSubData d) =>
      new(d.Variant, d.StartIndex, d.IsDisplayed, d.ParsedForm, d.VocabId.HasValue ? new VocabId(d.VocabId.Value) : null);

   /// Creates SentenceData from raw Anki NoteData (for NoteCache and Python interop paths).
   public static SentenceData FromAnkiNoteData(NoteData data) => FromAnki(new AnkiSentenceNote(data));

   public static SentenceData FromAnki(AnkiSentenceNote anki) =>
      new()
      {
         Id = (anki.Id ?? SentenceId.New()).Value,
         Tags = new List<string>(anki.Tags),
         SourceQuestion = anki.SourceQuestion,
         SourceAnswer = anki.SourceAnswer,
         SourceComments = anki.SourceComments,
         Reading = anki.Reading,
         ExternalId = anki.ExternalId,
         Audio = anki.Audio,
         Screenshot = anki.Screenshot,
      };

   /// Merges Anki-owned fields into existing data, preserving all fields Anki does not store.
   public SentenceData MergeAnkiData(NoteData ankiData) => this; //There are no fields where Anki owns the data

   public static ParsingResult CreateParsingResult(SentenceParsingResultSubData? data)
   {
      if(data == null) return new ParsingResult(new List<ParsedMatch>(), "", "");
      return new ParsingResult(
         data.ParsedWords.Select(FromParsedMatchSubData).ToList(),
         data.Sentence,
         data.ParserVersion);
   }

   public static SentenceConfiguration CreateConfiguration(SentenceConfigSubData? data, Action saveCallback)
   {
      if(data == null)
         return new SentenceConfiguration(
            new List<string>(),
            WordExclusionSet.Empty(saveCallback),
            WordExclusionSet.Empty(saveCallback));
      return new SentenceConfiguration(
         data.HighlightedWords.ToList(),
         new WordExclusionSet(saveCallback, data.IncorrectMatches.Select(FromExclusionSubData).ToList()),
         new WordExclusionSet(saveCallback, data.HiddenMatches.Select(FromExclusionSubData).ToList()));
   }

   static SentenceConfigSubData ToConfigSubData(SentenceConfiguration config) =>
      new()
      {
         HighlightedWords = config.HighlightedWords.ToList(),
         IncorrectMatches = config.IncorrectMatches.Get().Select(ToExclusionSubData).ToList(),
         HiddenMatches = config.HiddenMatches.Get().Select(ToExclusionSubData).ToList(),
      };

   static WordExclusionSubData ToExclusionSubData(WordExclusion ex) =>
      new() { Word = ex.Word, Index = ex.Index };

   static SentenceParsingResultSubData? ToParsingResultSubData(ParsingResult? result)
   {
      if(result == null || string.IsNullOrEmpty(result.Sentence)) return null;
      return new SentenceParsingResultSubData
             {
                Sentence = result.Sentence,
                ParserVersion = result.ParserVersion,
                ParsedWords = result.ParsedWords.Select(ToParsedMatchSubData).ToList(),
             };
   }

   static ParsedMatchSubData ToParsedMatchSubData(ParsedMatch match) =>
      new()
      {
         Variant = match.Variant,
         StartIndex = match.StartIndex,
         IsDisplayed = match.IsDisplayed,
         ParsedForm = match.ParsedForm,
         VocabId = match.VocabId?.Value,
      };
}

/// Sentence configuration sub-data (serialized in JSON).
[MemoryPackable]
public partial class SentenceConfigSubData
{
   public List<string> HighlightedWords { get; init; } = [];
   public List<WordExclusionSubData> IncorrectMatches { get; init; } = [];
   public List<WordExclusionSubData> HiddenMatches { get; init; } = [];
}

/// Word exclusion sub-data.
[MemoryPackable]
public partial class WordExclusionSubData
{
   public string Word { get; init; } = string.Empty;
   public int Index { get; init; } = -1;
}

/// Sentence parsing result sub-data (serialized in JSON).
[MemoryPackable]
public partial class SentenceParsingResultSubData
{
   public string Sentence { get; init; } = string.Empty;
   public string ParserVersion { get; init; } = string.Empty;
   public List<ParsedMatchSubData> ParsedWords { get; init; } = [];
}

/// Individual parsed match sub-data.
[MemoryPackable]
public partial class ParsedMatchSubData
{
   public string Variant { get; init; } = string.Empty;
   public int StartIndex { get; init; }
   public bool IsDisplayed { get; init; }
   public string ParsedForm { get; init; } = string.Empty;
   public Guid? VocabId { get; init; }
}
