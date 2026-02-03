using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Sentences;

public class SentenceConfiguration
{
    public List<string> HighlightedWords { get; }
    public WordExclusionSet IncorrectMatches { get; }
    public WordExclusionSet HiddenMatches { get; }

    public SentenceConfiguration(
        List<string> highlightedWords,
        WordExclusionSet incorrectMatches,
        WordExclusionSet hiddenMatches)
    {
        HighlightedWords = highlightedWords ?? new List<string>();
        IncorrectMatches = incorrectMatches ?? WordExclusionSet.Empty();
        HiddenMatches = hiddenMatches ?? WordExclusionSet.Empty();
    }

    public static SentenceConfiguration Empty()
    {
        return new SentenceConfiguration(
            new List<string>(),
            WordExclusionSet.Empty(),
            WordExclusionSet.Empty());
    }

    public override string ToString()
    {
        var parts = new List<string>();
        if (HighlightedWords.Any())
        {
            parts.Add($"highlighted_words: [{string.Join(", ", HighlightedWords)}]");
        }
        if (!IncorrectMatches.IsEmpty())
        {
            parts.Add($"incorrect_matches: {IncorrectMatches}");
        }
        if (!HiddenMatches.IsEmpty())
        {
            parts.Add($"hidden_matches: {HiddenMatches}");
        }
        return string.Join(", ", parts);
    }
}
