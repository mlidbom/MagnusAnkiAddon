using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Sentences;

public class ParsedMatch
{
    public string ParsedForm { get; set; }
    public int VocabId { get; set; }
    public bool IsDisplayed { get; set; }
    public int StartPosition { get; set; }
    public int EndPosition { get; set; }

    public ParsedMatch(string parsedForm, int vocabId, bool isDisplayed, int startPosition, int endPosition)
    {
        ParsedForm = parsedForm;
        VocabId = vocabId;
        IsDisplayed = isDisplayed;
        StartPosition = startPosition;
        EndPosition = endPosition;
    }

    public override string ToString()
    {
        return $"{ParsedForm}@{StartPosition}-{EndPosition} (vocab_id={VocabId}, displayed={IsDisplayed})";
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
