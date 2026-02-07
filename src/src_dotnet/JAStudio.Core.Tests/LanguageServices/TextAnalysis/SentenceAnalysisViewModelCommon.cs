using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Configuration;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.UI.Web.Sentence;
using Xunit;

namespace JAStudio.Core.Tests.LanguageServices.TextAnalysis;

public static class SentenceAnalysisViewModelCommon
{
   public static string SurfaceAndMatchForm(MatchViewModel matchVm)
   {
      var formToDisplay = matchVm.ParsedForm;
      if(matchVm.VocabMatch != null && matchVm.VocabMatch.Vocab.Question.IsDisambiguated)
      {
         formToDisplay = matchVm.VocabMatch.Vocab.Question.DisambiguationName;
      }

      var emergency = matchVm.Match.IsEmergencyDisplayed ? ":emergency" : "";
      return matchVm.DisplayVocabForm
                ? $"{formToDisplay}:{matchVm.VocabForm}{emergency}"
                : $"{formToDisplay}{emergency}";
   }

   public static void AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(string sentence,
                                                                                 List<WordExclusion> incorrect,
                                                                                 List<WordExclusion> hidden,
                                                                                 List<string> expectedOutput)
   {
      var sentenceNote = SentenceNote.Create(sentence);
      hidden.ForEach(sentenceNote.Configuration.HiddenMatches.Add);
      incorrect.ForEach(sentenceNote.Configuration.IncorrectMatches.Add);

      var sentenceViewModel = new SentenceViewModel(sentenceNote,
         TemporaryServiceCollection.Instance.ServiceLocator.Resolve<Settings>(),
         TemporaryServiceCollection.Instance.ServiceLocator.Resolve<VocabCollection>());

      void RunNoteAssertions(string message)
      {
         var rootWords = sentenceViewModel.DisplayedMatches.Select(SurfaceAndMatchForm).ToList();
         Assert.True(
            rootWords.SequenceEqual(expectedOutput),
            $"{message}\nExpected: [{string.Join(", ", expectedOutput)}]\nActual: [{string.Join(", ", rootWords)}]");
      }

      RunNoteAssertions(incorrect.Count == 0
                           ? "running assertions with no exclusions"
                           : "running assertions with exclusions");
   }

   public static void AssertDisplayWordsEqualWithIncorrectExclusions(string sentence, string[] incorrectStrings, params string[] expectedOutput) =>
      AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, incorrectStrings.Select(WordExclusion.FromString).ToList(), [], expectedOutput.ToList());

   public static void AssertDisplayWordsEqualWithHiddenExclusions(string sentence, string[] hiddenStrings, params string[] expectedOutput) =>
      AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, [], hiddenStrings.Select(WordExclusion.FromString).ToList(), expectedOutput.ToList());

   public static void AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(string sentence, params string[] expectedOutput) =>
      AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, [], [], expectedOutput.ToList());

   public static void AssertAllWordsEqual(string sentence, List<string> expectedOutput)
   {
      var sentenceNote = SentenceNote.Create(sentence);
      var analysis = new SentenceViewModel(sentenceNote,
         TemporaryServiceCollection.Instance.ServiceLocator.Resolve<Settings>(),
         TemporaryServiceCollection.Instance.ServiceLocator.Resolve<VocabCollection>());
      var candidateWords = analysis.Analysis.CandidateWords;
      var matches = candidateWords
                   .SelectMany(it => it.Matches)
                   .Select(SurfaceAndMatchForm)
                   .ToList();

      Assert.Equal(expectedOutput, matches);
   }

   public static void AssertAllWordsEqual(string sentence, params string[] expectedOutput) => AssertAllWordsEqual(sentence, expectedOutput.ToList());
}
