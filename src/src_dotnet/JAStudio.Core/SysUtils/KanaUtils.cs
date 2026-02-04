using System;
using System.Linq;

namespace JAStudio.Core.SysUtils;

public static class KanaUtils
{
    public const string FullWidthSpace = "　";

    public static string PadToLength(string value, int targetLength)
    {
        if (string.IsNullOrEmpty(value))
        {
            value = string.Empty;
        }

        var padding = Math.Max(0, targetLength - value.Length);
        return value + new string(FullWidthSpace[0], padding);
    }

    public static bool CharacterIsHiragana(char ch)
    {
        return ch >= 0x3040 && ch <= 0x309F;
    }

    public static bool CharacterIsKatakana(char ch)
    {
        return ch >= 0x30A0 && ch <= 0x30FF;
    }

    public static bool CharacterIsKana(char ch)
    {
        return CharacterIsHiragana(ch) || CharacterIsKatakana(ch);
    }

    public static bool CharacterIsKanji(char ch)
    {
        // CJK Unified Ideographs - Common and uncommon kanji (4E00 - 9FAF)
        // CJK Unified Ideographs Extension A - Rare kanji (3400 - 4DBF)
        var code = (int)ch;
        return (code >= 0x4E00 && code <= 0x9FAF) ||
               (code >= 0x3400 && code <= 0x4DBF);
    }

    public static bool IsOnlyKana(string text)
    {
        return text.All(CharacterIsKana);
    }

    public static bool IsOnlyHiragana(string text)
    {
        return text.All(CharacterIsHiragana);
    }

    public static bool IsOnlyKatakana(string text)
    {
        return text.All(CharacterIsKatakana);
    }

    public static string HiraganaToKatakana(string hiragana)
    {
        return new string(hiragana.Select(ch => 
            CharacterIsHiragana(ch) ? (char)(ch + 96) : ch
        ).ToArray());
    }

    public static string KatakanaToHiragana(string katakana)
    {
        return new string(katakana.Select(ch =>
            CharacterIsKatakana(ch) ? (char)(ch - 96) : ch
        ).ToArray());
    }

    public static string[] ExtractKanji(string text)
    {
        return text.Where(CharacterIsKanji).Select(ch => ch.ToString()).ToArray();
    }

    public static string Romanize(string text)
    {
        // TODO: Implement when pykakasi/romkan equivalent is available
        // For now, return the original text
        return text;
    }

    public static string RomajiToHiragana(string romaji)
    {
        // TODO: Implement when romkan equivalent is available
        return romaji;
    }

    public static string RomajiToKatakana(string romaji)
    {
        // TODO: Implement when romkan equivalent is available
        return romaji;
    }

    public static string AnythingToHiragana(string text)
    {
        return IsOnlyKana(text) ? KatakanaToHiragana(text) : RomajiToHiragana(text);
    }
}
