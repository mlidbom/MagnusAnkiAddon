using JAStudio.Core.Note;
using System;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches;

public abstract class Match
{
    public CandidateWordVariant Variant { get; protected set; } = null!;
    public int StartIndex { get; protected set; }
    public bool IsValidForDisplay { get; protected set; }
    public string ParsedForm { get; protected set; } = "";

    protected Match()
    {
    }
}

public class VocabMatch : Match
{
    public VocabNote Vocab { get; }

    public VocabMatch(VocabNote vocab)
    {
        Vocab = vocab;
    }
}

public class CandidateWordVariant
{
    public bool IsSurface { get; set; }
}

public class TextAnalysis
{
    public System.Collections.Generic.List<Match> ValidMatches { get; set; } = new();
    public string Text { get; set; } = "";
    public string Version { get; set; } = "";
}
