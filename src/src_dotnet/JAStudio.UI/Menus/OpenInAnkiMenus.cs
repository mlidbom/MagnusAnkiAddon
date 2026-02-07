using System;
using System.Collections.Generic;
using JAStudio.Core.AnkiUtils;
using JAStudio.UI.Anki;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds "Open in Anki" menus for searching notes in the Anki browser.
/// Ported from jastudio/ui/menus/open_in_anki.py
/// Now uses UI-agnostic MenuItem specifications and AnkiFacade for Anki calls.
/// </summary>
public static class OpenInAnkiMenus
{
    /// <summary>
    /// Build the complete "Open in Anki" menu structure as a UI-agnostic specification.
    /// Can be passed to AvaloniaMenuAdapter, PyQt adapter, or any other UI framework.
    /// </summary>
    /// <param name="getSearchText">Function that returns the text to search for</param>
    public static SpecMenuItem BuildOpenInAnkiMenuSpec(Func<string> getSearchText)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home2("Anki"),
            new List<SpecMenuItem>
            {
                BuildExactMatchesMenuSpec(getSearchText),
                BuildKanjiMenuSpec(getSearchText),
                BuildVocabMenuSpec(getSearchText),
                BuildSentenceMenuSpec(getSearchText)
            }
        );
    }

    /// <summary>
    /// Build the "Open in Anki" menu and convert to Avalonia MenuItem.
    /// This is a convenience method for backward compatibility.
    /// </summary>
    public static Avalonia.Controls.MenuItem BuildOpenInAnkiMenu(Func<string> getSearchText)
    {
        var spec = BuildOpenInAnkiMenuSpec(getSearchText);
        return AvaloniaMenuAdapter.ToAvalonia(spec);
    }

    private static SpecMenuItem BuildExactMatchesMenuSpec(Func<string> getSearchText)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1("Exact matches"),
            new List<SpecMenuItem>
            {
                CreateLookupSpec(ShortcutFinger.Home1("Open Exact matches | no sentences | reading cards"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.ExactMatchesNoSentencesReadingCards(getSearchText())),
                CreateLookupSpec(ShortcutFinger.Home2("Open Exact matches with sentences"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.ExactMatches(getSearchText()))
            }
        );
    }

    private static SpecMenuItem BuildKanjiMenuSpec(Func<string> getSearchText)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home2("Kanji"),
            new List<SpecMenuItem>
            {
                CreateLookupSpec(ShortcutFinger.Home1("All kanji in string"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.KanjiInString(getSearchText())),
                CreateLookupSpec(ShortcutFinger.Home2("By reading part"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.KanjiWithReadingPart(getSearchText())),
                CreateLookupSpec(ShortcutFinger.Home3("By reading exact"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.NotesLookup(Core.App.Col().Kanji.WithReading(getSearchText()))),
                CreateLookupSpec(ShortcutFinger.Home4("With radicals"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.KanjiWithRadicalsInString(getSearchText())),
                CreateLookupSpec(ShortcutFinger.Up1("With meaning"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.KanjiWithMeaning(getSearchText()))
            }
        );
    }

    private static SpecMenuItem BuildVocabMenuSpec(Func<string> getSearchText)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Vocab"),
            new List<SpecMenuItem>
            {
                CreateLookupSpec(ShortcutFinger.Home1("form -"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.SingleVocabByFormExact(getSearchText())),
                CreateLookupSpec(ShortcutFinger.Home2("form - read card only"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.SingleVocabByFormExactReadCardOnly(getSearchText())),
                CreateLookupSpec(ShortcutFinger.Home3("form, reading or answer"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.SingleVocabByQuestionReadingOrAnswerExact(getSearchText())),
                CreateLookupSpec(ShortcutFinger.Home4("Wildcard"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.SingleVocabWildcard(getSearchText())),
                CreateLookupSpec(ShortcutFinger.Up1("Text words"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.TextVocabLookup(getSearchText()))
            }
        );
    }

    private static SpecMenuItem BuildSentenceMenuSpec(Func<string> getSearchText)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home4("Sentence"),
            new List<SpecMenuItem>
            {
                CreateLookupSpec(ShortcutFinger.Home1("Parse Vocabulary"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.SentenceSearch(getSearchText(), exact: false)),
                CreateLookupSpec(ShortcutFinger.Home2("Exact String"), 
                    () => Core.TemporaryServiceCollection.Instance.QueryBuilder.SentenceSearch(getSearchText(), exact: true))
            }
        );
    }

    private static SpecMenuItem CreateLookupSpec(string header, Func<string> getQuery)
    {
        return SpecMenuItem.Command(
            header,
            () =>
            {
                var query = getQuery();
                AnkiFacade.ExecuteLookup(query);
            }
        );
    }
}

