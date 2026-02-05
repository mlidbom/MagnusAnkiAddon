using System;
using System.Collections.Generic;
using JAStudio.Core.AnkiUtils;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;
using SpecMenuItem = JAStudio.UI.Menus.UIAgnosticMenuStructure.MenuItem;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds "Open in Anki" menus for searching notes in the Anki browser.
/// Ported from jastudio/ui/menus/open_in_anki.py
/// Now uses UI-agnostic MenuItem specifications.
/// </summary>
public static class OpenInAnkiMenus
{
    /// <summary>
    /// Build the complete "Open in Anki" menu structure as a UI-agnostic specification.
    /// Can be passed to AvaloniaMenuAdapter, Python, or any other UI framework.
    /// </summary>
    /// <param name="getSearchText">Function that returns the text to search for</param>
    /// <param name="executeLookup">Action to execute an Anki search query</param>
    public static SpecMenuItem BuildOpenInAnkiMenuSpec(Func<string> getSearchText, Action<string> executeLookup)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home2("Anki"),
            new List<SpecMenuItem>
            {
                BuildExactMatchesMenuSpec(getSearchText, executeLookup),
                BuildKanjiMenuSpec(getSearchText, executeLookup),
                BuildVocabMenuSpec(getSearchText, executeLookup),
                BuildSentenceMenuSpec(getSearchText, executeLookup)
            }
        );
    }

    /// <summary>
    /// Build the "Open in Anki" menu and convert to Avalonia MenuItem.
    /// This is a convenience method for backward compatibility.
    /// </summary>
    public static Avalonia.Controls.MenuItem BuildOpenInAnkiMenu(Func<string> getSearchText, Action<string> executeLookup)
    {
        var spec = BuildOpenInAnkiMenuSpec(getSearchText, executeLookup);
        return AvaloniaMenuAdapter.ToAvalonia(spec);
    }

    private static SpecMenuItem BuildExactMatchesMenuSpec(Func<string> getSearchText, Action<string> executeLookup)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1("Exact matches"),
            new List<SpecMenuItem>
            {
                CreateLookupSpec(ShortcutFinger.Home1("Open Exact matches | no sentences | reading cards"), 
                    () => QueryBuilder.ExactMatchesNoSentencesReadingCards(getSearchText()), executeLookup),
                CreateLookupSpec(ShortcutFinger.Home2("Open Exact matches with sentences"), 
                    () => QueryBuilder.ExactMatches(getSearchText()), executeLookup)
            }
        );
    }

    private static SpecMenuItem BuildKanjiMenuSpec(Func<string> getSearchText, Action<string> executeLookup)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home2("Kanji"),
            new List<SpecMenuItem>
            {
                CreateLookupSpec(ShortcutFinger.Home1("All kanji in string"), 
                    () => QueryBuilder.KanjiInString(getSearchText()), executeLookup),
                CreateLookupSpec(ShortcutFinger.Home2("By reading part"), 
                    () => QueryBuilder.KanjiWithReadingPart(getSearchText()), executeLookup),
                CreateLookupSpec(ShortcutFinger.Home3("By reading exact"), 
                    () => QueryBuilder.NotesLookup(Core.App.Col().Kanji.WithReading(getSearchText())), executeLookup),
                CreateLookupSpec(ShortcutFinger.Home4("With radicals"), 
                    () => QueryBuilder.KanjiWithRadicalsInString(getSearchText()), executeLookup),
                CreateLookupSpec(ShortcutFinger.Up1("With meaning"), 
                    () => QueryBuilder.KanjiWithMeaning(getSearchText()), executeLookup)
            }
        );
    }

    private static SpecMenuItem BuildVocabMenuSpec(Func<string> getSearchText, Action<string> executeLookup)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Vocab"),
            new List<SpecMenuItem>
            {
                CreateLookupSpec(ShortcutFinger.Home1("form -"), 
                    () => QueryBuilder.SingleVocabByFormExact(getSearchText()), executeLookup),
                CreateLookupSpec(ShortcutFinger.Home2("form - read card only"), 
                    () => QueryBuilder.SingleVocabByFormExactReadCardOnly(getSearchText()), executeLookup),
                CreateLookupSpec(ShortcutFinger.Home3("form, reading or answer"), 
                    () => QueryBuilder.SingleVocabByQuestionReadingOrAnswerExact(getSearchText()), executeLookup),
                CreateLookupSpec(ShortcutFinger.Home4("Wildcard"), 
                    () => QueryBuilder.SingleVocabWildcard(getSearchText()), executeLookup),
                CreateLookupSpec(ShortcutFinger.Up1("Text words"), 
                    () => QueryBuilder.TextVocabLookup(getSearchText()), executeLookup)
            }
        );
    }

    private static SpecMenuItem BuildSentenceMenuSpec(Func<string> getSearchText, Action<string> executeLookup)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home4("Sentence"),
            new List<SpecMenuItem>
            {
                CreateLookupSpec(ShortcutFinger.Home1("Parse Vocabulary"), 
                    () => QueryBuilder.SentenceSearch(getSearchText(), exact: false), executeLookup),
                CreateLookupSpec(ShortcutFinger.Home2("Exact String"), 
                    () => QueryBuilder.SentenceSearch(getSearchText(), exact: true), executeLookup)
            }
        );
    }

    private static SpecMenuItem CreateLookupSpec(string header, Func<string> getQuery, Action<string> executeLookup)
    {
        return SpecMenuItem.Command(
            header,
            () =>
            {
                var query = getQuery();
                executeLookup(query);
            }
        );
    }
}

