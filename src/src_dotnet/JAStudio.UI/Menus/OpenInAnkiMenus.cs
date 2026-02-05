using System;
using System.Collections.Generic;
using Avalonia.Controls;
using JAStudio.Core.AnkiUtils;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds "Open in Anki" menus for searching notes in the Anki browser.
/// Ported from jastudio/ui/menus/open_in_anki.py
/// </summary>
public static class OpenInAnkiMenus
{
    /// <summary>
    /// Build the complete "Open in Anki" menu structure.
    /// </summary>
    /// <param name="getSearchText">Function that returns the text to search for</param>
    /// <param name="executeLookup">Action to execute an Anki search query</param>
    public static MenuItem BuildOpenInAnkiMenu(Func<string> getSearchText, Action<string> executeLookup)
    {
        return new MenuItem
        {
            Header = "Anki",
            ItemsSource = new List<MenuItem>
            {
                BuildExactMatchesMenu(getSearchText, executeLookup),
                BuildKanjiMenu(getSearchText, executeLookup),
                BuildVocabMenu(getSearchText, executeLookup),
                BuildSentenceMenu(getSearchText, executeLookup)
            }
        };
    }

    private static MenuItem BuildExactMatchesMenu(Func<string> getSearchText, Action<string> executeLookup)
    {
        return new MenuItem
        {
            Header = "Exact matches",
            ItemsSource = new List<MenuItem>
            {
                CreateLookupItem("Open Exact matches | no sentences | reading cards", 
                    () => QueryBuilder.ExactMatchesNoSentencesReadingCards(getSearchText()), executeLookup),
                CreateLookupItem("Open Exact matches with sentences", 
                    () => QueryBuilder.ExactMatches(getSearchText()), executeLookup)
            }
        };
    }

    private static MenuItem BuildKanjiMenu(Func<string> getSearchText, Action<string> executeLookup)
    {
        return new MenuItem
        {
            Header = "Kanji",
            ItemsSource = new List<MenuItem>
            {
                CreateLookupItem("All kanji in string", 
                    () => QueryBuilder.KanjiInString(getSearchText()), executeLookup),
                CreateLookupItem("By reading part", 
                    () => QueryBuilder.KanjiWithReadingPart(getSearchText()), executeLookup),
                CreateLookupItem("By reading exact", 
                    () => QueryBuilder.NotesLookup(Core.App.Col().Kanji.WithReading(getSearchText())), executeLookup),
                CreateLookupItem("With radicals", 
                    () => QueryBuilder.KanjiWithRadicalsInString(getSearchText()), executeLookup),
                CreateLookupItem("With meaning", 
                    () => QueryBuilder.KanjiWithMeaning(getSearchText()), executeLookup)
            }
        };
    }

    private static MenuItem BuildVocabMenu(Func<string> getSearchText, Action<string> executeLookup)
    {
        return new MenuItem
        {
            Header = "Vocab",
            ItemsSource = new List<MenuItem>
            {
                CreateLookupItem("form -", 
                    () => QueryBuilder.SingleVocabByFormExact(getSearchText()), executeLookup),
                CreateLookupItem("form - read card only", 
                    () => QueryBuilder.SingleVocabByFormExactReadCardOnly(getSearchText()), executeLookup),
                CreateLookupItem("form, reading or answer", 
                    () => QueryBuilder.SingleVocabByQuestionReadingOrAnswerExact(getSearchText()), executeLookup),
                CreateLookupItem("Wildcard", 
                    () => QueryBuilder.SingleVocabWildcard(getSearchText()), executeLookup),
                CreateLookupItem("Text words", 
                    () => QueryBuilder.TextVocabLookup(getSearchText()), executeLookup)
            }
        };
    }

    private static MenuItem BuildSentenceMenu(Func<string> getSearchText, Action<string> executeLookup)
    {
        return new MenuItem
        {
            Header = "Sentence",
            ItemsSource = new List<MenuItem>
            {
                CreateLookupItem("Parse Vocabulary", 
                    () => QueryBuilder.SentenceSearch(getSearchText(), exact: false), executeLookup),
                CreateLookupItem("Exact String", 
                    () => QueryBuilder.SentenceSearch(getSearchText(), exact: true), executeLookup)
            }
        };
    }

    private static MenuItem CreateLookupItem(string header, Func<string> getQuery, Action<string> executeLookup)
    {
        var item = new MenuItem { Header = header };
        item.Click += (s, e) =>
        {
            var query = getQuery();
            executeLookup(query);
        };
        return item;
    }
}
