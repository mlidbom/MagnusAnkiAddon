using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.ViewModels.KanjiList;

namespace JAStudio.Core.UI.Web.Kanji;

class KanjiListRenderer
{
   readonly KanjiCollection _kanji;
   internal KanjiListRenderer(KanjiCollection kanji) => _kanji = kanji;

   public string RenderList(JPNote note, List<KanjiNote> kanjis, List<string> kanjiReadings)
   {
      if(kanjis.Count == 0)
         return "";

      string HighlightInheritedReading(string text)
      {
         foreach(var reading in kanjiReadings)
         {
            var hiragana = KanaUtils.KatakanaToHiragana(reading);
            var katakana = KanaUtils.HiraganaToKatakana(reading);

            text = Regex.Replace(text,
                                 $@"\b{Regex.Escape(hiragana)}\b",
                                 $"<inherited-reading>{hiragana}</inherited-reading>");
            text = Regex.Replace(text,
                                 $@"\b{Regex.Escape(katakana)}\b",
                                 $"<inherited-reading>{katakana}</inherited-reading>");
         }

         return text;
      }

      int PreferStudyingKanji(KanjiNote kan) => kan.IsStudying() ? 0 : 1;

      kanjis = kanjis.Where(kan => kan != note).ToList();
      kanjis = kanjis.OrderBy(PreferStudyingKanji).ToList();

      var viewmodels = kanjis.Select(kanji => new KanjiViewModel(kanji)).ToList();

      var kanjiItems = viewmodels.Select(kanji => $$$"""
                                                             <div class="kanji_item {{{string.Join(" ", kanji.Kanji.GetMetaTags())}}}">
                                                                 <div class="kanji_main">
                                                                     <span class="kanji_kanji clipboard">{{{kanji.Question()}}}</span>
                                                                     <span class="kanji_readings">{{{HighlightInheritedReading(kanji.Readings())}}}</span>
                                                                     <span class="kanji_answer">{{{kanji.Answer()}}}</span>
                                                                 </div>
                                                                 <div class="kanji_mnemonic">{{{kanji.Mnemonic()}}}</div>
                                                             </div>
                                                     """);

      return $"""
              <div id="kanji_list" class="page_section">
                  <div class="page_section_title">kanji</div>
              {string.Join("\n", kanjiItems)}
              </div>
              """;
   }

   public string KanjiKanjiList(KanjiNote kanji)
   {
      var kanjis = _kanji.WithRadical(kanji.GetQuestion());
      var kanjiReadings = kanji.ReadingsClean;

      return RenderList(kanji, kanjis, kanjiReadings);
   }
}
