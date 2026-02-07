using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;

namespace JAStudio.Core.UI.Web.Vocab;

public class VocabSentenceMatchViewModel
{
    public ParsedMatch Match { get; }
    public VocabSentenceViewModel SentenceViewModel { get; }

    public VocabSentenceMatchViewModel(ParsedMatch match, VocabSentenceViewModel sentenceViewModel)
    {
        Match = match;
        SentenceViewModel = sentenceViewModel;
    }

    public bool IsDisplayed => Match.IsDisplayed;
    public int StartIndex => Match.StartIndex;
    public int EndIndex => Match.EndIndex;

    public bool IsPrimaryFormOf(VocabNote vocab)
    {
        return Match.ParsedForm == vocab.Question.WithoutNoiseCharacters;
    }

    public ParsedMatch? ShadedBy
    {
        get
        {
            var allParsedWords = SentenceViewModel.Result.ParsedWords.ToList();
            allParsedWords.Reverse();
            var shading = allParsedWords
                .Where(match => match.IsDisplayed && match.StartIndex <= StartIndex && StartIndex <= match.EndIndex)
                .ToList();

            return shading.Any() ? shading[0] : null;
        }
    }

    public ParsedMatch? YieldsTo
    {
        get
        {
            var yieldsTo = SentenceViewModel.Result.ParsedWords
                .Where(match => match.IsDisplayed &&
                               StartIndex < match.StartIndex &&
                               match.StartIndex <= EndIndex &&
                               EndIndex < match.EndIndex)
                .ToList();

            return yieldsTo.Any() ? yieldsTo[0] : null;
        }
    }

    public override string ToString()
    {
        return Match.ToString() ?? string.Empty;
    }
}

public class VocabSentenceViewModel
{
    public VocabNote Vocab { get; }
    public SentenceNote Sentence { get; }
    public ParsingResult Result { get; }
    public List<VocabSentenceMatchViewModel> Matches { get; }
    public List<VocabSentenceMatchViewModel> DisplayedMatches { get; }
    public HashSet<SentenceNote> HighlightedSentences { get; }
    public List<VocabSentenceMatchViewModel> ShadedMatches { get; }
    public HashSet<int> MatchedVocabIds { get; }

    public VocabSentenceViewModel(VocabNote vocabNote, SentenceNote sentenceNote)
    {
        Vocab = vocabNote;
        Sentence = sentenceNote;
        Result = sentenceNote.ParsingResult.Get();
        Matches = Result.ParsedWords
            .Where(match => match.VocabId == vocabNote.GetId())
            .Select(match => new VocabSentenceMatchViewModel(match, this))
            .ToList();
        DisplayedMatches = Matches.Where(match => match.IsDisplayed).ToList();
        HighlightedSentences = vocabNote.Sentences.UserHighlighted().ToHashSet();
        ShadedMatches = Matches.Where(match => !match.IsDisplayed).ToList();
        MatchedVocabIds = Result.ParsedWords.Select(match => match.VocabId).ToHashSet();
    }

    public VocabSentenceMatchViewModel PrimaryMatch =>
        DisplayedMatches.Any() ? DisplayedMatches[0] : Matches[0];

    public string FormatSentence()
    {
        var result = Result;
        var match = PrimaryMatch;
        var isPrimary = match.IsPrimaryFormOf(Vocab) ? "primary" : "secondary";
        var matchClass = $"{isPrimary}FormMatch";

        if (match.IsDisplayed)
        {
            var head = result.Sentence.Substring(0, match.StartIndex);
            var matchRange = result.Sentence.Substring(match.StartIndex, match.EndIndex - match.StartIndex);
            var tail = result.Sentence.Substring(match.EndIndex);
            return $"{head}<span class=\"vocabInContext {matchClass}\">{matchRange}</span>{tail}";
        }
        else
        {
            var shadingMatch = match.ShadedBy;

            var shadingStartIndex = shadingMatch?.StartIndex ?? match.StartIndex;
            var shadingEndIndex = shadingMatch?.EndIndex ?? match.EndIndex;

            var preCoveringMatchClass = shadingMatch != null && Vocab.RelatedNotes.InCompoundIds.Contains(shadingMatch.VocabId)
                ? "compound"
                : "shadingMatch";
            var postCoveringMatchClass = preCoveringMatchClass;

            var yieldsTo = match.YieldsTo;
            if (yieldsTo != null)
            {
                shadingEndIndex = yieldsTo.EndIndex;
                postCoveringMatchClass = "yieldsTo";
            }

            var sentenceText = result.Sentence;
            var minStart = System.Math.Min(shadingStartIndex, match.StartIndex);
            var maxEnd = System.Math.Max(shadingEndIndex, match.EndIndex);

            var head = sentenceText.Substring(0, minStart);
            var shadingPreRange = sentenceText.Substring(shadingStartIndex, match.StartIndex - shadingStartIndex);
            var matchRange = sentenceText.Substring(match.StartIndex, match.EndIndex - match.StartIndex);
            var shadingPostRange = sentenceText.Substring(match.EndIndex, shadingEndIndex - match.EndIndex);
            var tail = sentenceText.Substring(maxEnd);

            return string.Concat(
                head,
                $"<span class=\"vocabInContext {matchClass} {preCoveringMatchClass}\">{shadingPreRange}</span>",
                $"<span class=\"vocabInContext {matchClass}\">{matchRange}</span>",
                $"<span class=\"vocabInContext {matchClass} {postCoveringMatchClass}\">{shadingPostRange}</span>",
                tail);
        }
    }

    public bool IsHighlighted()
    {
        return HighlightedSentences.Contains(Sentence);
    }

    public bool VocabIsDisplayed => DisplayedMatches.Any();

    public string SentenceClasses()
    {
        var classes = "";
        if (HighlightedSentences.Contains(Sentence)) classes += "highlighted ";
        classes += string.Join(" ", Sentence.GetMetaTags());
        return classes;
    }

    public bool ContainsPrimaryForm()
    {
        return DisplayedMatches.Any(match => match.IsPrimaryFormOf(Vocab));
    }
}
