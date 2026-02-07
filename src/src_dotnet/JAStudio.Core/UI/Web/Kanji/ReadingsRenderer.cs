using JAStudio.Core.Note;
using System.Linq;
using JAStudio.Core.LanguageServices;

namespace JAStudio.Core.UI.Web.Kanji;

public static class ReadingsRenderer
{
    public static string RenderKatakanaOnyomi(KanjiNote kanjiNote)
    {
        var onReadingsList = kanjiNote.GetReadingOnListHtml()
            .Select(KanaUtils.HiraganaToKatakana)
            .ToList();
        var onReadings = string.Join(", ", onReadingsList.Select(reading => 
            $"""<span class="clipboard">{reading}</span>"""));
        var kunReadings = string.Join(", ", kanjiNote.GetReadingKunListHtml().Select(reading => 
            $"""<span class="clipboard">{reading}</span>"""));
        var nanReadings = string.Join(", ", kanjiNote.GetReadingNanListHtml().Select(reading => 
            $"""<span class="clipboard">{reading}</span>"""));

        return $"""
     <span class="reading">{onReadings}</span> <span class="readingsSeparator">|</span>
     <span class="reading">{kunReadings}</span> <span class="readingsSeparator">|</span>
     <span class="reading">{nanReadings}</span>
""";
    }
}
