using System.Linq;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Kanji;

static class ReadingsRenderer
{
   public static string RenderKatakanaOnyomi(KanjiNote kanjiNote)
   {
      var onReadingsList = kanjiNote.ReadingOnListHtml
                                    .Select(KanaUtils.HiraganaToKatakana)
                                    .ToList();
      var onReadings = string.Join(", ",
                                   onReadingsList.Select(reading =>
                                                            $"""<span class="clipboard">{reading}</span>"""));
      var kunReadings = string.Join(", ",
                                    kanjiNote.ReadingKunListHtml.Select(reading =>
                                                                           $"""<span class="clipboard">{reading}</span>"""));
      var nanReadings = string.Join(", ",
                                    kanjiNote.ReadingNanListHtml.Select(reading =>
                                                                           $"""<span class="clipboard">{reading}</span>"""));

      return $"""
                   <span class="reading">{onReadings}</span> <span class="readingsSeparator">|</span>
                   <span class="reading">{kunReadings}</span> <span class="readingsSeparator">|</span>
                   <span class="reading">{nanReadings}</span>
              """;
   }
}
