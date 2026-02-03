using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Sentences;

public class ParsedMatch
{
    public const int MissingNoteId = -1;
    
    public string Variant { get; set; }
    public int StartIndex { get; set; }
    public bool IsDisplayed { get; set; }
    public string ParsedForm { get; set; }
    public int VocabId { get; set; }

    public int EndIndex => StartIndex + ParsedForm.Length;

    public ParsedMatch(string variant, int startIndex, bool isDisplayed, string parsedForm, int vocabId)
    {
        Variant = variant;
        StartIndex = startIndex;
        IsDisplayed = isDisplayed;
        ParsedForm = parsedForm;
        VocabId = vocabId;
    }

    // Legacy constructor for compatibility
    public ParsedMatch(string parsedForm, int vocabId, bool isDisplayed, int startPosition, int endPosition)
        : this("S", startPosition, isDisplayed, parsedForm, vocabId)
    {
    }

    public override string ToString()
    {
        return $"{ParsedForm}@{StartIndex}-{EndIndex} (vocab_id={VocabId}, displayed={IsDisplayed}, variant={Variant})";
    }
}

public class ParsingResult
{
    public List<ParsedMatch> ParsedWords { get; }
    public string Sentence { get; }
    public string ParserVersion { get; }

    public ParsingResult(List<ParsedMatch> words, string sentence, string parserVersion)
    {
        ParsedWords = words ?? new List<ParsedMatch>();
        Sentence = sentence?.Replace(StringExtensions.InvisibleSpace, string.Empty) ?? string.Empty;
        ParserVersion = parserVersion ?? string.Empty;
    }

    public HashSet<int> MatchedVocabIds
    {
        get
        {
            return ParsedWords
                .Where(p => p.VocabId != -1)
                .Select(p => p.VocabId)
                .ToHashSet();
        }
    }

    public List<string> ParsedWordsStrings()
    {
        return ParsedWords.Select(p => p.ParsedForm).Distinct().ToList();
    }

    public static ParsingResult Empty()
    {
        return new ParsingResult(new List<ParsedMatch>(), string.Empty, "0");
    }
}
