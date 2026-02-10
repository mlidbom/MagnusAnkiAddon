using JAStudio.Core.LanguageServices;
using JAStudio.Core.Note;

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
        var readings = $"{KanaUtils.HiraganaToKatakana(Kanji.ReadingOnHtml)} <span class=\"readingsSeparator\">|</span> {Kanji.ReadingKunHtml}";
        if (!string.IsNullOrEmpty(Kanji.ReadingNanHtml))
        {
            readings += $" <span class=\"readingsSeparator\">|</span> {Kanji.ReadingNanHtml}";
        }
        return readings;
    }

    public string Mnemonic()
    {
        return Kanji.ActiveMnemonic;
    }

    public override string ToString()
    {
        return $"{Question()}      {StringExtensions.PadToLength(Answer(), 60)}: {Readings()}";
    }
}
