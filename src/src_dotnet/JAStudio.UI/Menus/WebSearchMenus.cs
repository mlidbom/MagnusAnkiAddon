using System;
using System.Collections.Generic;
using System.Web;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;

namespace JAStudio.UI.Menus;

public static class WebSearchMenus
{
   public static SpecMenuItem BuildWebSearchMenuSpec(Func<string> getSearchText) =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home3("Web"),
         new List<SpecMenuItem>
         {
            BuildKanjiMenuSpec(getSearchText),
            BuildSentencesMenuSpec(getSearchText),
            BuildMiscMenuSpec(getSearchText),
            BuildLookupMenuSpec(getSearchText)
         });

   static SpecMenuItem BuildKanjiMenuSpec(Func<string> getSearchText) =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home1("Kanji"),
         new List<SpecMenuItem>
         {
            CreateWebLookupSpec(ShortcutFinger.Home1("Kanji explosion"), "https://kurumi.com/jp/kjbh/?k=%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home2("Kanji: Kanshudo"), "https://www.kanshudo.com/search?q=%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home3("Kanji map"), "https://thekanjimap.com/index.php?k=%s", getSearchText)
         }
      );

   static SpecMenuItem BuildSentencesMenuSpec(Func<string> getSearchText) =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home2("Sentences"),
         new List<SpecMenuItem>
         {
            CreateWebLookupSpec(ShortcutFinger.Home1("Sentences: Immersion Kit"), "https://www.immersionkit.com/dictionary?exact=true&sort=sentence_length%3Aasc&keyword=%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home2("Sentences: Tatoeba"), "https://tatoeba.org/en/sentences/search?from=jpn&to=eng&query=%s", getSearchText)
         }
      );

   static SpecMenuItem BuildMiscMenuSpec(Func<string> getSearchText) =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home3("Misc"),
         new List<SpecMenuItem>
         {
            BuildConjugateMenuSpec(getSearchText),
            BuildTranslateMenuSpec(getSearchText),
            BuildGrammarMenuSpec(getSearchText),
            BuildImagesMenuSpec(getSearchText)
         }
      );

   static SpecMenuItem BuildConjugateMenuSpec(Func<string> getSearchText) =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home1("Conjugate"),
         new List<SpecMenuItem>
         {
            CreateWebLookupSpec(ShortcutFinger.Home1("Conjugate: Japanese verb conjugator"), "https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home2("Conjugate: Verbix"), "https://www.verbix.com/webverbix/japanese/%s", getSearchText)
         }
      );

   static SpecMenuItem BuildTranslateMenuSpec(Func<string> getSearchText) =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home2("Translate"),
         new List<SpecMenuItem>
         {
            CreateWebLookupSpec(ShortcutFinger.Home1("Translate: Deepl"), "https://www.deepl.com/en/translator#ja/en/%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home2("Translate: Kanshudo"), "https://www.kanshudo.com/sentence_translate?q=%s", getSearchText)
         }
      );

   static SpecMenuItem BuildGrammarMenuSpec(Func<string> getSearchText) =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home3("Grammar"),
         new List<SpecMenuItem>
         {
            CreateWebLookupSpec(ShortcutFinger.Home1("Grammar: Google"), "https://www.google.com/search?q=japanese+grammar+%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home2("Grammar: Japanese with anime"), "https://www.google.com/search?q=site:www.japanesewithanime.com+%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home3("Grammar: Wiktionary"), "https://en.wiktionary.org/wiki/%s", getSearchText)
         }
      );

   static SpecMenuItem BuildImagesMenuSpec(Func<string> getSearchText) =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home4("Images"),
         new List<SpecMenuItem>
         {
            CreateWebLookupSpec(ShortcutFinger.Home1("Images: Google"), "https://www.google.com/search?udm=2&tbs=sur:cl&q=%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home2("Images: Bing"), "https://www.bing.com/images/search?qft=+filterui:licenseType-Any&q=%s", getSearchText)
         }
      );

   static SpecMenuItem BuildLookupMenuSpec(Func<string> getSearchText) =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home4("Lookup"),
         new List<SpecMenuItem>
         {
            CreateWebLookupSpec(ShortcutFinger.Home1("English: Merriam Webster"), "https://www.merriam-webster.com/dictionary/%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home2("Wiktionary"), "https://en.wiktionary.org/wiki/%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home3("Lookup: Takoboto"), "https://takoboto.jp/?q=%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Home4("Lookup: Jisho"), "https://jisho.org/search/%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Up1("Lookup: Wanikani"), "https://www.wanikani.com/search?query=%s", getSearchText),
            CreateWebLookupSpec(ShortcutFinger.Down1("Lookup: Word Kanshudo"), "https://www.kanshudo.com/searchw?q=%s", getSearchText)
         }
      );

   static SpecMenuItem CreateWebLookupSpec(string header, string urlTemplate, Func<string> getSearchText) =>
      SpecMenuItem.Command(header, () => BrowserLauncher.OpenUrl(urlTemplate.Replace("%s", HttpUtility.UrlEncode(getSearchText()))));
}
