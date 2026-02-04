using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.UI.Web.Sentence;
using Xunit;

namespace JAStudio.Core.Tests.LanguageServices.TextAnalysis;

/// <summary>
/// Helper methods ported from test_sentence_analysis_viewmodel_common.py
/// </summary>
public static class SentenceAnalysisViewModelCommon
{
    public static string SurfaceAndMatchForm(MatchViewModel matchVm)
    {
        var formToDisplay = matchVm.ParsedForm;
        if (matchVm.VocabMatch != null && matchVm.VocabMatch.Vocab.Question.IsDisambiguated)
        {
            formToDisplay = matchVm.VocabMatch.Vocab.Question.DisambiguationName;
        }

        var emergency = matchVm.Match.IsEmergencyDisplayed ? ":emergency" : "";
        return matchVm.DisplayVocabForm
            ? $"{formToDisplay}:{matchVm.VocabForm}{emergency}"
            : $"{formToDisplay}{emergency}";
    }

    public static void AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(
        string sentence, 
        List<WordExclusion> excluded, 
        List<string> expectedOutput)
    {
        var sentenceNote = SentenceNote.Create(sentence);
        if (excluded.Count != 0)
        {
            sentenceNote.Configuration.SetValueDirectlyTestsOnly(SentenceConfiguration.FromHiddenMatches(excluded));
        }

        var sentenceViewModel = new SentenceViewModel(sentenceNote);

        void RunNoteAssertions(string message)
        {
            var rootWords = sentenceViewModel.DisplayedMatches.Select(SurfaceAndMatchForm).ToList();
            Assert.True(
                rootWords.SequenceEqual(expectedOutput),
                $"{message}\nExpected: [{string.Join(", ", expectedOutput)}]\nActual: [{string.Join(", ", rootWords)}]");
        }

        if (excluded.Count == 0)
        {
            RunNoteAssertions("running assertions with no exclusions");
        }
        else
        {
            RunNoteAssertions("running assertions with exclusions hidden");

            sentenceNote.Configuration.SetValueDirectlyTestsOnly(SentenceConfiguration.FromIncorrectMatches(excluded));
            sentenceViewModel = new SentenceViewModel(sentenceNote);
            RunNoteAssertions("running assertions with exclusions marked as incorrect matches");
        }
    }

    /// <summary>
    /// Overload that accepts string arrays for exclusions in format "word:index" or "word".
    /// </summary>
    public static void AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(
        string sentence, 
        string[] exclusionStrings, 
        params string[] expectedOutput)
    {
        var excluded = exclusionStrings.Select(WordExclusion.FromString).ToList();
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, excluded, expectedOutput.ToList());
    }

    /// <summary>
    /// Overload for tests with no exclusions.
    /// </summary>
    public static void AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(
        string sentence, 
        params string[] expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput.ToList());
    }

    public static void AssertAllWordsEqual(string sentence, List<string> expectedOutput)
    {
        var sentenceNote = SentenceNote.Create(sentence);
        var analysis = new SentenceViewModel(sentenceNote);
        var candidateWords = analysis.Analysis.CandidateWords;
        var matches = candidateWords
            .SelectMany(cand => cand.Matches)
            .Select(SurfaceAndMatchForm)
            .ToList();

        Assert.Equal(expectedOutput, matches);
    }

    /// <summary>
    /// Overload that accepts params array for expected output.
    /// </summary>
    public static void AssertAllWordsEqual(string sentence, params string[] expectedOutput)
    {
        AssertAllWordsEqual(sentence, expectedOutput.ToList());
    }
}
