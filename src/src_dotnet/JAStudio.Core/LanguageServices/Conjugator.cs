using JAStudio.Core.Note;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.LanguageServices;

public static class Conjugator
{
    private static readonly List<string> IchidanEndings = new() { "", "ろ", "な" };

    private static readonly List<string> GodanRuEndings = new() { "り", "ら", "れ", "っ" };
    private static readonly List<string> GodanRuOrIchidanEndings;

    public static readonly Dictionary<string, string> GodanPotentialVerbEndingToDictionaryFormEndings = new()
    {
        { "える", "う" },
        { "ける", "く" },
        { "げる", "ぐ" },
        { "せる", "す" },
        { "てる", "つ" },
        { "ねる", "ぬ" },
        { "べる", "ぶ" },
        { "める", "む" },
        { "れる", "る" }
    };

    public static readonly HashSet<string> GodanImperativeVerbEndings = new()
    {
        "え", "け", "げ", "せ", "て", "ね", "べ", "め", "れ"
    };

    private const int IStemIndex = 0;
    private const int AStemIndex = 1;
    private const int EStemIndex = 2;
    private const int TeStemIndex = 3;

    private static readonly Dictionary<string, List<string>> OneCharacterMappings = new()
    {
        { "う", new List<string> { "い", "わ", "え", "っ" } },
        { "く", new List<string> { "き", "か", "け", "い" } },
        { "ぐ", new List<string> { "ぎ", "が", "げ", "い" } },
        { "す", new List<string> { "し", "さ", "せ", "し" } },
        { "つ", new List<string> { "ち", "た", "て", "っ" } },
        { "ぬ", new List<string> { "に", "な", "ね", "ん" } },
        { "ぶ", new List<string> { "び", "ば", "べ", "ん" } },
        { "む", new List<string> { "み", "ま", "め", "ん" } },
        { "る", GodanRuEndings },
        { "い", new List<string> { "く", "け", "か" } } // I adjective stems
    };

    private static readonly Dictionary<string, List<string>> TwoCharacterMappings = new()
    {
        { "する", new List<string> { "し", "さ", "すれ", "し", "せ" } },
        { "くる", new List<string> { "き", "こ", "くれ", "き" } },
        { "いく", new List<string> { "いき", "いか", "いけ", "いっ", "いこ" } },
        { "行く", new List<string> { "行き", "行か", "行け", "行っ", "行こ" } },
        { "ます", new List<string> { "まし", "ませ" } },
        { "いい", new List<string> { "よく", "よけ", "よか", "よかっ" } }
    };

    private static readonly List<string> MasuFormsByIndex = new() { "まし", "ませ", "まし", "まし" };

    private static readonly HashSet<string> AruVerbs = new()
    {
        "なさる", "くださる", "おっしゃる", "ござる", "らっしゃる", "下さる", "為さる"
    };

    private static readonly Dictionary<string, List<string>> AruMappings = new()
    {
        { "さる", new List<string> { "さい", "さら", "され", "さっ" } },
        { "ざる", new List<string> { "ざい", "ざら", "ざれ", "ざっ" } },
        { "ゃる", new List<string> { "ゃい", "ゃら", "れば", "ゃっ" } }
    };

    static Conjugator()
    {
        GodanRuOrIchidanEndings = new List<string>(GodanRuEndings);
        GodanRuOrIchidanEndings.AddRange(IchidanEndings);
    }

    public static string ConstructRootVerbForPossiblyPotentialGodanVerbDictionaryForm(string potentialVerbForm)
    {
        var ending = potentialVerbForm.Substring(potentialVerbForm.Length - 2);
        return potentialVerbForm.Substring(0, potentialVerbForm.Length - 2) + 
               GodanPotentialVerbEndingToDictionaryFormEndings[ending];
    }

    private static bool IsAruVerb(string word)
    {
        return AruVerbs.Any(aruEnding => word.EndsWith(aruEnding));
    }

    public static List<string> GetWordStems(string word, bool isIchidanVerb = false, bool isGodan = false)
    {
        try
        {
            if (IsAruVerb(word))
            {
                var ending = word.Substring(word.Length - 2);
                return AruMappings[ending].Select(end => word.Substring(0, word.Length - 2) + end).ToList();
            }

            if (isIchidanVerb)
            {
                return IchidanEndings.Select(end => word.Substring(0, word.Length - 1) + end).ToList();
            }

            if (isGodan)
            {
                var lastChar = word.Substring(word.Length - 1);
                return OneCharacterMappings[lastChar].Select(end => word.Substring(0, word.Length - 1) + end).ToList();
            }

            var lastTwoChars = word.Length >= 2 ? word.Substring(word.Length - 2) : "";
            if (TwoCharacterMappings.ContainsKey(lastTwoChars))
            {
                return TwoCharacterMappings[lastTwoChars].Select(end => word.Substring(0, word.Length - 2) + end).ToList();
            }

            var lastOneChar = word.Substring(word.Length - 1);
            if (OneCharacterMappings.ContainsKey(lastOneChar))
            {
                if (lastOneChar == "る")
                {
                    return GodanRuOrIchidanEndings.Select(end => word.Substring(0, word.Length - 1) + end).ToList();
                }
                return OneCharacterMappings[lastOneChar].Select(end => word.Substring(0, word.Length - 1) + end).ToList();
            }
        }
        catch (KeyNotFoundException)
        {
            MyLog.Warning($"GetWordStems failed to handle {word}, returning empty list");
        }
        catch (System.ArgumentOutOfRangeException)
        {
            MyLog.Warning($"GetWordStems failed to handle {word}, returning empty list");
        }

        return new List<string> { word };
    }

    private static string GetStem(string word, int stemIndex, bool isIchidanVerb = false, bool isGodan = false)
    {
        try
        {
            if (IsAruVerb(word))
            {
                var ending = word.Substring(word.Length - 2);
                return word.Substring(0, word.Length - 2) + AruMappings[ending][stemIndex];
            }

            if (isIchidanVerb)
            {
                return word.Substring(0, word.Length - 1);
            }

            if (isGodan)
            {
                var lastChar = word.Substring(word.Length - 1);
                return word.Substring(0, word.Length - 1) + OneCharacterMappings[lastChar][stemIndex];
            }

            var lastTwoChars = word.Length >= 2 ? word.Substring(word.Length - 2) : "";
            if (lastTwoChars == "ます")
            {
                return word.Substring(0, word.Length - 2) + MasuFormsByIndex[stemIndex];
            }

            if (TwoCharacterMappings.ContainsKey(lastTwoChars))
            {
                return word.Substring(0, word.Length - 2) + TwoCharacterMappings[lastTwoChars][stemIndex];
            }

            var lastOneChar = word.Substring(word.Length - 1);
            if (OneCharacterMappings.ContainsKey(lastOneChar))
            {
                if (lastOneChar != "る")
                {
                    return word.Substring(0, word.Length - 1) + OneCharacterMappings[lastOneChar][stemIndex];
                }
                return word.Substring(0, word.Length - 1) + OneCharacterMappings[lastOneChar][stemIndex];
            }
        }
        catch (KeyNotFoundException)
        {
            MyLog.Warning($"GetStem failed to handle {word}, returning word as-is");
        }
        catch (System.ArgumentOutOfRangeException)
        {
            MyLog.Warning($"GetStem failed to handle {word}, returning word as-is");
        }

        return word;
    }

    public static List<string> GetVocabStems(VocabNote vocab)
    {
        return GetWordStems(vocab.GetQuestion(), vocab.PartsOfSpeech.IsIchidan(), vocab.PartsOfSpeech.IsGodan());
    }

    public static string GetIStem(string word, bool isIchidan = false, bool isGodan = false)
    {
        return GetStem(word, IStemIndex, isIchidan, isGodan);
    }

    public static string GetAStem(string word, bool isIchidan = false, bool isGodan = false)
    {
        return GetStem(word, AStemIndex, isIchidan, isGodan);
    }

    public static string GetEStem(string word, bool isIchidan = false, bool isGodan = false)
    {
        if (isIchidan)
        {
            return word.Substring(0, word.Length - 1) + "れ";
        }
        return GetStem(word, EStemIndex, isIchidan, isGodan);
    }

    public static string GetTeStem(string word, bool isIchidan = false, bool isGodan = false)
    {
        return GetStem(word, TeStemIndex, isIchidan, isGodan);
    }

    public static string GetIStemVocab(VocabNote vocab, string form = "")
    {
        var word = !string.IsNullOrEmpty(form) ? form : vocab.GetQuestion();
        return GetIStem(word, vocab.PartsOfSpeech.IsIchidan(), vocab.PartsOfSpeech.IsGodan());
    }

    public static string GetEStemVocab(VocabNote vocab, string form = "")
    {
        var word = !string.IsNullOrEmpty(form) ? form : vocab.GetQuestion();
        return GetEStem(word, vocab.PartsOfSpeech.IsIchidan(), vocab.PartsOfSpeech.IsGodan());
    }

    public static string GetAStemVocab(VocabNote vocab, string form = "")
    {
        var word = !string.IsNullOrEmpty(form) ? form : vocab.GetQuestion();
        return GetAStem(word, vocab.PartsOfSpeech.IsIchidan(), vocab.PartsOfSpeech.IsGodan());
    }

    public static string GetTeStemVocab(VocabNote vocab, string form = "")
    {
        var word = !string.IsNullOrEmpty(form) ? form : vocab.GetQuestion();
        return GetTeStem(word, vocab.PartsOfSpeech.IsIchidan(), vocab.PartsOfSpeech.IsGodan());
    }

    public static string GetImperative(string word, bool isIchidan = false, bool isGodan = false)
    {
        if (isGodan || (!isIchidan && !word.EndsWith("る")))
        {
            return GetEStem(word, isIchidan, isGodan);
        }

        return word.Substring(0, word.Length - 1) + "ろ";
    }
}
