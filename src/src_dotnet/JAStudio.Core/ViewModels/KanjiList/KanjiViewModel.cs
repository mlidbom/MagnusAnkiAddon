using JAStudio.Core.Note;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.ViewModels.KanjiList;

public class KanjiViewModel
{
    public KanjiNote Kanji { get; }

    public KanjiViewModel(KanjiNote kanji)
    {
        Kanji = kanji;
    }

    public string Question()
    {
        return Kanji.GetQuestion();
    }

    public string Answer()
    {
        return Kanji.GetAnswer();
    }

    public string Readings()
    {
        var readings = $"{KanaUtils.HiraganaToKatakana(Kanji.GetReadingOnHtml())} <span class=\"readingsSeparator\">|</span> {Kanji.GetReadingKunHtml()}";
        if (!string.IsNullOrEmpty(Kanji.GetReadingNanHtml()))
        {
            readings += $" <span class=\"readingsSeparator\">|</span> {Kanji.GetReadingNanHtml()}";
        }
        return readings;
    }

    public string Mnemonic()
    {
        return Kanji.GetActiveMnemonic();
    }

    public override string ToString()
    {
        return $"{Question()}      {StringExtensions.PadToLength(Answer(), 60)}: {Readings()}";
    }
}
