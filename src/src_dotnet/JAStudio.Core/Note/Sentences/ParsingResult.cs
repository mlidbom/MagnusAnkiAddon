using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;

namespace JAStudio.Core.Note.Sentences;

public class ParsingResult
{
   public List<ParsedMatch> ParsedWords { get; }
   public string Sentence { get; }
   public string ParserVersion { get; }

   public ParsingResult(List<ParsedMatch> words, string sentence, string parserVersion)
   {
      ParsedWords = words;
      Sentence = sentence?.Replace(StringExtensions.InvisibleSpace, string.Empty) ?? string.Empty;
      ParserVersion = parserVersion ?? string.Empty;
   }

   public HashSet<NoteId> MatchedVocabIds
   {
      get
      {
         return ParsedWords
               .Where(p => p.VocabId != null)
               .Select(p => p.VocabId!)
               .ToHashSet();
      }
   }

   public List<string> ParsedWordsStrings()
   {
      return ParsedWords.Select(p => p.ParsedForm).Distinct().ToList();
   }

   public static ParsingResult FromAnalysis(TextAnalysis analysis) =>
      new(
         analysis.ValidMatches.Select(ParsedMatch.FromMatch).ToList(),
         analysis.Text,
         TextAnalysis.Version
      );
}
