using System.Linq;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.Note;

public class DifficultyCalculator
{
    private readonly double _startingSeconds;
    private readonly double _hiraganaSeconds;
    private readonly double _katakataSeconds;
    private readonly double _kanjiSeconds;

    public DifficultyCalculator(double startingSeconds, double hiraganaSeconds, double katakataSeconds, double kanjiSeconds)
    {
        _startingSeconds = startingSeconds;
        _hiraganaSeconds = hiraganaSeconds;
        _katakataSeconds = katakataSeconds;
        _kanjiSeconds = kanjiSeconds;
    }

    public static bool IsOtherCharacter(char ch)
    {
        return !KanaUtils.CharacterIsKana(ch) && !KanaUtils.CharacterIsKanji(ch);
    }

    public double AllowedSeconds(string text)
    {
        if (string.IsNullOrEmpty(text))
        {
            return _startingSeconds;
        }

        var hiraganaCount = text.Count(KanaUtils.CharacterIsHiragana);
        var katakanaCount = text.Count(KanaUtils.CharacterIsKatakana);
        var kanjiCount = text.Count(KanaUtils.CharacterIsKanji);
        var otherCount = text.Count(IsOtherCharacter);

        var hiraganaSeconds = hiraganaCount * _hiraganaSeconds;
        var katakanaSeconds = katakanaCount * _katakataSeconds;
        var kanjiSeconds = kanjiCount * _kanjiSeconds;
        var otherCharacterSeconds = otherCount * _hiraganaSeconds;

        return _startingSeconds + hiraganaSeconds + katakanaSeconds + kanjiSeconds + otherCharacterSeconds;
    }
}
