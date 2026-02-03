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

public class WordExclusionSet
{
    public List<WordExclusion> Exclusions { get; }

    public WordExclusionSet(List<WordExclusion> exclusions)
    {
        Exclusions = exclusions ?? new List<WordExclusion>();
    }

    public static WordExclusionSet Empty()
    {
        return new WordExclusionSet(new List<WordExclusion>());
    }

    public bool IsEmpty() => !Exclusions.Any();

    public List<string> Words()
    {
        return Exclusions.Select(e => e.Word).ToList();
    }

    public override string ToString()
    {
        return $"[{string.Join(", ", Exclusions)}]";
    }
}

public class WordExclusion
{
    public string Word { get; set; }
    public int? Position { get; set; }

    public WordExclusion(string word, int? position = null)
    {
        Word = word;
        Position = position;
    }

    public override string ToString()
    {
        return Position.HasValue ? $"{Word}@{Position}" : Word;
    }
}
