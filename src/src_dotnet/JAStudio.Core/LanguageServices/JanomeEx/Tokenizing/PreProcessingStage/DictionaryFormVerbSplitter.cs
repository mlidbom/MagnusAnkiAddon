using System.Collections.Generic;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing.PreProcessingStage;

public static class DictionaryFormVerbSplitter
{
    public static List<IAnalysisToken>? TrySplit(JNToken token)
    {
        if (token.IsDictionaryForm() && !token.IsProgressiveForm())
        {
            if (token.IsIchidanVerb)
            {
                return SplitIchidanDictionaryForm(token);
            }

            if (token.IsGodanVerb)
            {
                return SplitGodanDictionaryForm(token);
            }

            if (token.IsKuruVerb)
            {
                return SplitKuruVerb(token);
            }

            if (token.IsSuruVerb)
            {
                return SplitSuruVerb(token);
            }
        }

        return null;
    }

    static List<IAnalysisToken> SplitIchidanDictionaryForm(JNToken token)
    {
        var ichidanSurface = token.Surface[..^1];
        return
        [
           new IchidanDictionaryFormStem(token, ichidanSurface, token.BaseForm),
           new IchidanDictionaryFormInflection(token)
        ];
    }

    static List<IAnalysisToken> SplitGodanDictionaryForm(JNToken token)
    {
        var godanSurface = token.Surface[..^1];
        var godanDictionaryEnding = token.Surface[^1..];
        return
        [
           new GodanDictionaryFormStem(token, godanSurface, token.BaseForm),
           new GodanDictionaryFormInflection(token, godanDictionaryEnding, "う")
        ];
    }

    static List<IAnalysisToken> SplitKuruVerb(JNToken token)
    {
        var surface = token.Surface[..^1];
        return
        [
           new KuruVerbDictionaryFormStem(token, surface, token.BaseForm),
           new KuruVerbDictionaryFormInflection(token)
        ];
    }

    static List<IAnalysisToken> SplitSuruVerb(JNToken token)
    {
        var surface = token.Surface[..^1];
        return
        [
           new SuruVerbDictionaryFormStem(token, surface, token.BaseForm),
           new SuruVerbDictionaryFormInflection(token)
        ];
    }
}
