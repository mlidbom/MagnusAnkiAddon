using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.UI.Web.Sentence;

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

    public static void AssertDisplayWordsEqual(string sentence, List<string> expectedOutput)
    {
        var sentenceNote = SentenceNote.Create(sentence);
        var sentenceViewModel = new SentenceViewModel(sentenceNote);

        var rootWords = sentenceViewModel.DisplayedMatches.Select(SurfaceAndMatchForm).ToList();
        if (!rootWords.SequenceEqual(expectedOutput))
        {
            throw new Xunit.Sdk.XunitException(
                $"Expected: [{string.Join(", ", expectedOutput)}]\nActual: [{string.Join(", ", rootWords)}]");
        }
    }
}
