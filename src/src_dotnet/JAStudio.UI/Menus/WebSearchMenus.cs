using System;
using System.Collections.Generic;
using System.Web;
using Avalonia.Controls;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds web search menus for looking up Japanese text on various websites.
/// Ported from jastudio/ui/menus/web_search.py
/// </summary>
public static class WebSearchMenus
{
    /// <summary>
    /// Build the complete web search menu structure.
    /// </summary>
    /// <param name="getSearchText">Function that returns the text to search for</param>
    /// <param name="openUrl">Action to open a URL in the browser</param>
    public static MenuItem BuildWebSearchMenu(Func<string> getSearchText, Action<string> openUrl)
    {
        return new MenuItem
        {
            Header = "Web",
            ItemsSource = new List<MenuItem>
            {
                BuildKanjiMenu(getSearchText, openUrl),
                BuildSentencesMenu(getSearchText, openUrl),
                BuildMiscMenu(getSearchText, openUrl),
                BuildLookupMenu(getSearchText, openUrl)
            }
        };
    }

    private static MenuItem BuildKanjiMenu(Func<string> getSearchText, Action<string> openUrl)
    {
        return new MenuItem
        {
            Header = "Kanji",
            ItemsSource = new List<MenuItem>
            {
                CreateWebLookupItem("Kanji explosion", "https://www.kurumi.com/jp/kjbh/?k=%s", getSearchText, openUrl),
                CreateWebLookupItem("Kanshudo", "https://www.kanshudo.com/search?q=%s", getSearchText, openUrl),
                CreateWebLookupItem("Kanji map", "https://thekanjimap.com/%s", getSearchText, openUrl)
            }
        };
    }

    private static MenuItem BuildSentencesMenu(Func<string> getSearchText, Action<string> openUrl)
    {
        return new MenuItem
        {
            Header = "Sentences",
            ItemsSource = new List<MenuItem>
            {
                CreateWebLookupItem("Sentences: Immersion Kit", "https://www.immersionkit.com/dictionary?exact=true&sort=sentence_length%3Aasc&keyword=%s", getSearchText, openUrl),
                CreateWebLookupItem("Sentences: Tatoeba", "https://tatoeba.org/en/sentences/search?from=jpn&to=eng&query=%s", getSearchText, openUrl)
            }
        };
    }

    private static MenuItem BuildMiscMenu(Func<string> getSearchText, Action<string> openUrl)
    {
        return new MenuItem
        {
            Header = "Misc",
            ItemsSource = new List<MenuItem>
            {
                BuildConjugateMenu(getSearchText, openUrl),
                BuildTranslateMenu(getSearchText, openUrl),
                BuildGrammarMenu(getSearchText, openUrl),
                BuildImagesMenu(getSearchText, openUrl)
            }
        };
    }

    private static MenuItem BuildConjugateMenu(Func<string> getSearchText, Action<string> openUrl)
    {
        return new MenuItem
        {
            Header = "Conjugate",
            ItemsSource = new List<MenuItem>
            {
                CreateWebLookupItem("Conjugate: Japanese verb conjugator", "https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s", getSearchText, openUrl),
                CreateWebLookupItem("Conjugate: Verbix", "https://www.verbix.com/webverbix/japanese/%s", getSearchText, openUrl)
            }
        };
    }

    private static MenuItem BuildTranslateMenu(Func<string> getSearchText, Action<string> openUrl)
    {
        return new MenuItem
        {
            Header = "Translate",
            ItemsSource = new List<MenuItem>
            {
                CreateWebLookupItem("Translate: Deepl", "https://www.deepl.com/en/translator#ja/en/%s", getSearchText, openUrl),
                CreateWebLookupItem("Translate: Kanshudo", "https://www.kanshudo.com/sentence_translate?q=%s", getSearchText, openUrl)
            }
        };
    }

    private static MenuItem BuildGrammarMenu(Func<string> getSearchText, Action<string> openUrl)
    {
        return new MenuItem
        {
            Header = "Grammar",
            ItemsSource = new List<MenuItem>
            {
                CreateWebLookupItem("Grammar: Google", "https://www.google.com/search?q=japanese+grammar+%s", getSearchText, openUrl),
                CreateWebLookupItem("Grammar: Japanese with anime", "https://www.google.com/search?q=site:www.japanesewithanime.com+%s", getSearchText, openUrl),
                CreateWebLookupItem("Grammar: Wiktionary", "https://en.wiktionary.org/wiki/%s", getSearchText, openUrl)
            }
        };
    }

    private static MenuItem BuildImagesMenu(Func<string> getSearchText, Action<string> openUrl)
    {
        return new MenuItem
        {
            Header = "Images",
            ItemsSource = new List<MenuItem>
            {
                CreateWebLookupItem("Images: Google", "https://www.google.com/search?udm=2&tbs=sur:cl&q=%s", getSearchText, openUrl),
                CreateWebLookupItem("Images: Bing", "https://www.bing.com/images/search?qft=+filterui:licenseType-Any&q=%s", getSearchText, openUrl)
            }
        };
    }

    private static MenuItem BuildLookupMenu(Func<string> getSearchText, Action<string> openUrl)
    {
        return new MenuItem
        {
            Header = "Lookup",
            ItemsSource = new List<MenuItem>
            {
                CreateWebLookupItem("English: Merriam Webster", "https://www.merriam-webster.com/dictionary/%s", getSearchText, openUrl),
                CreateWebLookupItem("Wiktionary", "https://en.wiktionary.org/wiki/%s", getSearchText, openUrl),
                CreateWebLookupItem("Lookup: Takoboto", "https://takoboto.jp/?q=%s", getSearchText, openUrl),
                CreateWebLookupItem("Lookup: Jisho", "https://jisho.org/search/%s", getSearchText, openUrl),
                CreateWebLookupItem("Lookup: Wanikani", "https://www.wanikani.com/search?query=%s", getSearchText, openUrl),
                CreateWebLookupItem("Lookup: Word Kanshudo", "https://www.kanshudo.com/searchw?q=%s", getSearchText, openUrl)
            }
        };
    }

    private static MenuItem CreateWebLookupItem(string header, string urlTemplate, Func<string> getSearchText, Action<string> openUrl)
    {
        var item = new MenuItem { Header = header };
        item.Click += (s, e) =>
        {
            var searchText = getSearchText();
            var encodedText = HttpUtility.UrlEncode(searchText);
            var url = urlTemplate.Replace("%s", encodedText);
            openUrl(url);
        };
        return item;
    }
}
