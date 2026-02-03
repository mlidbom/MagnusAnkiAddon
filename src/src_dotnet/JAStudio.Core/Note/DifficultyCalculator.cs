using System.Linq;

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
        // TODO: Implement character_is_kana and character_is_kanji when KanaUtils is ported
        return !char.IsLetterOrDigit(ch) && !char.IsWhiteSpace(ch);
    }

    public double AllowedSeconds(string text)
    {
        if (string.IsNullOrEmpty(text))
        {
            return _startingSeconds;
        }

        // TODO: Implement proper character classification when KanaUtils is ported
        var hiraganaCount = 0;
        var katakanaCount = 0;
        var kanjiCount = 0;
        var otherCount = 0;

        foreach (var ch in text)
        {
            if (IsOtherCharacter(ch))
            {
                otherCount++;
            }
            // Placeholder - will be properly implemented when KanaUtils is available
        }

        var hiraganaSeconds = hiraganaCount * _hiraganaSeconds;
        var katakanaSeconds = katakanaCount * _katakataSeconds;
        var kanjiSeconds = kanjiCount * _kanjiSeconds;
        var otherCharacterSeconds = otherCount * _hiraganaSeconds;

        return _startingSeconds + hiraganaSeconds + katakanaSeconds + kanjiSeconds + otherCharacterSeconds;
    }
}
