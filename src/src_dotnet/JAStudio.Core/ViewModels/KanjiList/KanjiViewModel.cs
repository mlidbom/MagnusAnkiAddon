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
        var readings = $"{KanaUtils.HiraganaToKatakana(Kanji.ReadingOnHtml.Value)} <span class=\"readingsSeparator\">|</span> {Kanji.ReadingKunHtml.Value}";
        if (!string.IsNullOrEmpty(Kanji.ReadingNanHtml.Value))
        {
            readings += $" <span class=\"readingsSeparator\">|</span> {Kanji.ReadingNanHtml.Value}";
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
