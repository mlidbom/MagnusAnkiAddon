using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing.PreProcessingStage;

public static class IchidanGodanPotentialOrImperativeHybridSplitter
{
   static readonly HashSet<string> PotentialOrImperativeGodanLastCompoundParts = ["える", "え"];

    public static List<IAnalysisToken>? TrySplit(JNToken token, VocabCollection vocabs)
    {
        if (Equals(token.InflectedForm, InflectionForms.ImperativeMeireikei.Ro))
        {
            return null;
        }

        var hiddenGodan = TryFindGodanHiddenInIchidanUsingDictionary(token) ??
                          TryFindVocabBasedPotentialOrImperativeGodanCompound(token, vocabs);

        if (hiddenGodan != null)
        {
            if (IsPotentialGodan(token, hiddenGodan))
            {
                return SplitGodanPotential(token, hiddenGodan);
            }
            if (IsImperativeGodan(token, hiddenGodan))
            {
                return SplitGodanImperative(token, hiddenGodan);
            }
        }

        return null;
    }

    static List<IAnalysisToken> SplitGodanImperative(JNToken token, string godanBase)
    {
        if (Equals(token.InflectedForm, InflectionForms.ImperativeMeireikei.Yo))
        {
            // Handles cases like 放せよ which janome turns into a single token and believes is an ichidan よ imperative
            var godanSurface = token.Surface[..^2];
            var imperativePart = token.Surface[^2..^1];
            return
            [
               new SplitToken(token, godanSurface, godanBase, isInflectableWord: true, isGodanImperativeStem: true),
               new SplitToken(token, imperativePart, "え", isInflectableWord: true, isGodanImperativeInflection: true),
               new SplitToken(token, "よ", "よ", isInflectableWord: false)
            ];
        }
        else
        {
            var godanSurface = token.Surface[..^1];
            var imperativePart = token.Surface[^1..];
            var imperativeBase = imperativePart == "い" ? "い" : "え";
            return
            [
               new SplitToken(token, godanSurface, godanBase, isInflectableWord: true, isGodanImperativeStem: true),
               new SplitToken(token, imperativePart, imperativeBase, isInflectableWord: true, isGodanImperativeInflection: true)
            ];
        }
    }

    static List<IAnalysisToken> SplitGodanPotential(JNToken token, string godanBase)
    {
        var isDictionaryForm = token.Surface.EndsWith("る");

        var basePart = token.Surface.TrimEnd('る')[..^1];
        var potentialSurface = token.Surface.Substring(basePart.Length);
        var potentialBase = isDictionaryForm ? potentialSurface : potentialSurface + "る";

        if (isDictionaryForm)
        {
            potentialSurface = potentialSurface[..^1];
            return
            [
               new GodanPotentialDictionaryFormStem(token, basePart, godanBase),
               new GodanPotentialInflectionDictionaryFormStem(token, potentialSurface, potentialBase),
               new GodanPotentialInflectionDictionaryFormInflection(token)
            ];
        }

        return
        [
           new SplitToken(token, basePart, godanBase, isInflectableWord: true, isGodanPotentialStem: true),
           new SplitToken(token, potentialSurface, potentialBase, isInflectableWord: true, isGodanPotentialInflection: true)
        ];
    }

    static string? TryFindVocabBasedPotentialOrImperativeGodanCompound(JNToken token, VocabCollection vocabs)
    {
        foreach (var vocab in vocabs.WithQuestion(token.BaseForm))
        {
            var compoundParts = vocab.CompoundParts.All();
            if (compoundParts.Count == 2 && PotentialOrImperativeGodanLastCompoundParts.Contains(compoundParts[1]))
            {
                if (WordInfo.IsGodan(compoundParts[0]))
                {
                    return compoundParts[0];
                }
            }
        }
        return null;
    }

    static bool IsPotentialGodan(JNToken token, string godanBase)
    {
        if (token.Surface.EndsWith("る") || (token.Next != null && token.Next.IsValidGodanPotentialFormInflection()))
        {
            var godanDictEntry = WordInfo.LookupGodan(godanBase);
            if (godanDictEntry == null)
            {
                return false;
            }

            // Intransitive verbs don't take を so this is most likely actually the ichidan verb
            if (godanDictEntry.IsIntransitive && token.Previous != null && token.Previous.Surface == "を" &&
                WordInfo.IsIchidan(token.BaseForm))
            {
                return false;
            }
            return true;
        }
        return false;
    }

    static bool IsImperativeGodan(JNToken token, string godanBase)
    {
        if (!Conjugator.GodanImperativeVerbEndings.Contains(token.Surface[^1..]) &&
            !Equals(token.InflectedForm, InflectionForms.ImperativeMeireikei.Yo))
        {
            return false;
        }

        var godanWordInfo = WordInfo.Lookup(godanBase);
        if (WordInfo.Lookup(token.BaseForm) == null)
        {
            // We check for potential godan before this, so if there is no ichidan verb in the dictionary,
            // the only thing left is an imperative godan
            return true;
        }
        else if (godanWordInfo != null && godanWordInfo.IsIntransitive && token.Previous != null && token.Previous.Surface == "を")
        {
            // Intransitive verbs don't take を so this is most likely actually the ichidan verb
            return false;
        }
        else if (token.Next != null && token.Next.CannotFollowIchidanStem())
        {
            return true;
        }
        else if (token.Next == null || token.IsEndOfStatement)
        {
            return true;
        }
        else if (Equals(token.InflectedForm, InflectionForms.ImperativeMeireikei.Yo))
        {
            // Handles cases like 放せよ which janome turns into a single token and believes is an ichidan よ imperative
            return true;
        }
        else if (token.Next != null && token.Next.IsMoreLikelyToFollowImperativeThanIchidanStem())
        {
            return true;
        }

        return false;
    }

    public static bool BaseFormHasGodanPotentialEnding(string baseForm)
    {
        if (baseForm.Length < 2)
        {
            return false;
        }

        var ending = baseForm[^2..];
        return Conjugator.GodanPotentialVerbEndingToDictionaryFormEndings.ContainsKey(ending);
    }

    static string? TryFindGodanHiddenInIchidanUsingDictionary(JNToken token)
    {
        if (token.BaseForm.Length >= 2 &&
            BaseFormHasGodanPotentialEnding(token.BaseForm) &&
            token.IsIchidanVerb)
        {
            var possibleGodanForm = Conjugator.ConstructRootVerbForPossiblyPotentialGodanVerbDictionaryForm(token.BaseForm);
            if (WordInfo.IsGodan(possibleGodanForm))
            {
                return possibleGodanForm;
            }
        }
        return null;
    }

    public static bool IsIchidanHidingGodan(VocabNote vocab) => TryGetGodanHiddenByIchidan(vocab) != null;

    public static WordInfoEntry? TryGetGodanHiddenByIchidan(VocabNote vocab)
    {
        var question = vocab.GetQuestion();
        if (BaseFormHasGodanPotentialEnding(question))
        {
            var possibleGodanForm = Conjugator.ConstructRootVerbForPossiblyPotentialGodanVerbDictionaryForm(question);
            var godanDictEntry = WordInfo.LookupGodan(possibleGodanForm);
            if (godanDictEntry != null && godanDictEntry.IsGodan)
            {
                return godanDictEntry;
            }
        }
        return null;
    }
}
