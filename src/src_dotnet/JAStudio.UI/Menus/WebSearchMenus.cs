using System;
using System.Collections.Generic;
using System.Web;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;
using SpecMenuItem = JAStudio.UI.Menus.UIAgnosticMenuStructure.MenuItem;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds web search menus for looking up Japanese text on various websites.
/// Ported from jastudio/ui/menus/web_search.py
/// Now uses UI-agnostic MenuItem specifications.
/// </summary>
public static class WebSearchMenus
{
    /// <summary>
    /// Build the complete web search menu structure as a UI-agnostic specification.
    /// Can be passed to AvaloniaMenuAdapter, Python, or any other UI framework.
    /// </summary>
    /// <param name="getSearchText">Function that returns the text to search for</param>
    /// <param name="openUrl">Action to open a URL in the browser</param>
    public static SpecMenuItem BuildWebSearchMenuSpec(Func<string> getSearchText, Action<string> openUrl)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Web"),
            new List<SpecMenuItem>
            {
                BuildKanjiMenuSpec(getSearchText, openUrl),
                BuildSentencesMenuSpec(getSearchText, openUrl),
                BuildMiscMenuSpec(getSearchText, openUrl),
                BuildLookupMenuSpec(getSearchText, openUrl)
            }
        );
    }

    /// <summary>
    /// Build the web search menu and convert to Avalonia MenuItem.
    /// This is a convenience method for backward compatibility.
    /// </summary>
    public static Avalonia.Controls.MenuItem BuildWebSearchMenu(Func<string> getSearchText, Action<string> openUrl)
    {
        var spec = BuildWebSearchMenuSpec(getSearchText, openUrl);
        return AvaloniaMenuAdapter.ToAvalonia(spec);
    }

    private static SpecMenuItem BuildKanjiMenuSpec(Func<string> getSearchText, Action<string> openUrl)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1("Kanji"),
            new List<SpecMenuItem>
            {
                CreateWebLookupSpec(ShortcutFinger.Home1("Kanji explosion"), "https://www.kurumi.com/jp/kjbh/?k=%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home2("Kanshudo"), "https://www.kanshudo.com/search?q=%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home3("Kanji map"), "https://thekanjimap.com/%s", getSearchText, openUrl)
            }
        );
    }

    private static SpecMenuItem BuildSentencesMenuSpec(Func<string> getSearchText, Action<string> openUrl)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home2("Sentences"),
            new List<SpecMenuItem>
            {
                CreateWebLookupSpec(ShortcutFinger.Home1("Sentences: Immersion Kit"), "https://www.immersionkit.com/dictionary?exact=true&sort=sentence_length%3Aasc&keyword=%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home2("Sentences: Tatoeba"), "https://tatoeba.org/en/sentences/search?from=jpn&to=eng&query=%s", getSearchText, openUrl)
            }
        );
    }

    private static SpecMenuItem BuildMiscMenuSpec(Func<string> getSearchText, Action<string> openUrl)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Misc"),
            new List<SpecMenuItem>
            {
                BuildConjugateMenuSpec(getSearchText, openUrl),
                BuildTranslateMenuSpec(getSearchText, openUrl),
                BuildGrammarMenuSpec(getSearchText, openUrl),
                BuildImagesMenuSpec(getSearchText, openUrl)
            }
        );
    }

    private static SpecMenuItem BuildConjugateMenuSpec(Func<string> getSearchText, Action<string> openUrl)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1("Conjugate"),
            new List<SpecMenuItem>
            {
                CreateWebLookupSpec(ShortcutFinger.Home1("Conjugate: Japanese verb conjugator"), "https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home2("Conjugate: Verbix"), "https://www.verbix.com/webverbix/japanese/%s", getSearchText, openUrl)
            }
        );
    }

    private static SpecMenuItem BuildTranslateMenuSpec(Func<string> getSearchText, Action<string> openUrl)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home2("Translate"),
            new List<SpecMenuItem>
            {
                CreateWebLookupSpec(ShortcutFinger.Home1("Translate: Deepl"), "https://www.deepl.com/en/translator#ja/en/%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home2("Translate: Kanshudo"), "https://www.kanshudo.com/sentence_translate?q=%s", getSearchText, openUrl)
            }
        );
    }

    private static SpecMenuItem BuildGrammarMenuSpec(Func<string> getSearchText, Action<string> openUrl)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Grammar"),
            new List<SpecMenuItem>
            {
                CreateWebLookupSpec(ShortcutFinger.Home1("Grammar: Google"), "https://www.google.com/search?q=japanese+grammar+%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home2("Grammar: Japanese with anime"), "https://www.google.com/search?q=site:www.japanesewithanime.com+%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home3("Grammar: Wiktionary"), "https://en.wiktionary.org/wiki/%s", getSearchText, openUrl)
            }
        );
    }

    private static SpecMenuItem BuildImagesMenuSpec(Func<string> getSearchText, Action<string> openUrl)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home4("Images"),
            new List<SpecMenuItem>
            {
                CreateWebLookupSpec(ShortcutFinger.Home1("Images: Google"), "https://www.google.com/search?udm=2&tbs=sur:cl&q=%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home2("Images: Bing"), "https://www.bing.com/images/search?qft=+filterui:licenseType-Any&q=%s", getSearchText, openUrl)
            }
        );
    }

    private static SpecMenuItem BuildLookupMenuSpec(Func<string> getSearchText, Action<string> openUrl)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home4("Lookup"),
            new List<SpecMenuItem>
            {
                CreateWebLookupSpec(ShortcutFinger.Home1("English: Merriam Webster"), "https://www.merriam-webster.com/dictionary/%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home2("Wiktionary"), "https://en.wiktionary.org/wiki/%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home3("Lookup: Takoboto"), "https://takoboto.jp/?q=%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Home4("Lookup: Jisho"), "https://jisho.org/search/%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Up1("Lookup: Wanikani"), "https://www.wanikani.com/search?query=%s", getSearchText, openUrl),
                CreateWebLookupSpec(ShortcutFinger.Down1("Lookup: Word Kanshudo"), "https://www.kanshudo.com/searchw?q=%s", getSearchText, openUrl)
            }
        );
    }

    private static SpecMenuItem CreateWebLookupSpec(string header, string urlTemplate, Func<string> getSearchText, Action<string> openUrl)
    {
        return SpecMenuItem.Command(
            header,
            () =>
            {
                var searchText = getSearchText();
                var encodedText = HttpUtility.UrlEncode(searchText);
                var url = urlTemplate.Replace("%s", encodedText);
                openUrl(url);
            }
        );
    }
}
