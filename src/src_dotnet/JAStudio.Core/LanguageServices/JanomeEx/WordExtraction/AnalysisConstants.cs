using System.Collections.Generic;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;

public static class AnalysisConstants
{
    public static readonly HashSet<string> RealQuoteCharacters = new() { "「", "」", "\"" };
    public static readonly HashSet<string> PseudoQuoteCharacters = new() { "と", "って" };
    public static readonly HashSet<string> AllQuoteCharacters;

    public static readonly HashSet<string> SpaceCharacters = new() { " ", "\t", StringExtensions.InvisibleSpace };

    public static readonly HashSet<string> QuestionMarks = new() { "？", "?" };
    public static readonly HashSet<string> Periods = new() { ".", "。", "｡" };
    public static readonly HashSet<string> Commas = new() { ",", "、" };
    public static readonly HashSet<string> Tilde = new() { "～", "~" };
    public static readonly HashSet<string> Exclamations = new() { "!" }; // TODO: Full-width exclamation mark?

    public static readonly HashSet<string> AllPunctuationCharacters;
    public static readonly HashSet<string> SentenceStartCharacters;
    public static readonly HashSet<string> SentenceEndCharacters;
    public static readonly HashSet<string> NoiseCharacters;

    public static readonly HashSet<string> PassiveVerbEndings = new() { "あれる", "られる", "される" };
    public static readonly HashSet<string> CausativeVerbEndings = new() { "あせる", "させる", "あす", "さす" };

    static AnalysisConstants()
    {
        AllQuoteCharacters = new HashSet<string>(RealQuoteCharacters);
        AllQuoteCharacters.UnionWith(PseudoQuoteCharacters);

        AllPunctuationCharacters = new HashSet<string>(AllQuoteCharacters);
        AllPunctuationCharacters.UnionWith(QuestionMarks);
        AllPunctuationCharacters.UnionWith(Periods);
        AllPunctuationCharacters.UnionWith(Commas);
        AllPunctuationCharacters.UnionWith(Exclamations);
        AllPunctuationCharacters.UnionWith(Tilde);
        AllPunctuationCharacters.UnionWith(new[] { ":", ";", "/", "|" });

        SentenceStartCharacters = new HashSet<string>(RealQuoteCharacters);
        SentenceStartCharacters.UnionWith(SpaceCharacters);
        SentenceStartCharacters.UnionWith(QuestionMarks);
        SentenceStartCharacters.UnionWith(Periods);

        SentenceEndCharacters = new HashSet<string>(AllQuoteCharacters);
        SentenceEndCharacters.UnionWith(SpaceCharacters);
        SentenceEndCharacters.UnionWith(QuestionMarks);
        SentenceEndCharacters.UnionWith(Periods);

        NoiseCharacters = new HashSet<string>(AllPunctuationCharacters);
        NoiseCharacters.UnionWith(SpaceCharacters);
        NoiseCharacters.UnionWith(PseudoQuoteCharacters);
        NoiseCharacters.UnionWith(SentenceEndCharacters);
    }
}
