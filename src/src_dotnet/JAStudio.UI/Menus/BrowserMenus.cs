using System;
using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.UI.Anki;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds browser context menu for Anki's card browser.
/// Corresponds to ui/menus/browser/main.py in Python.
/// </summary>
public static class BrowserMenus
{
    /// <summary>
    /// Build the complete browser context menu structure as UI-agnostic specifications.
    /// </summary>
    /// <param name="selectedCardIds">List of selected card IDs (from Python/Anki)</param>
    /// <param name="selectedNoteIds">List of selected note IDs (from Python/Anki)</param>
    public static SpecMenuItem BuildBrowserMenuSpec(dynamic selectedCardIds, dynamic selectedNoteIds)
    {
        var cardIds = ConvertToLongList(selectedCardIds);
        var noteIds = ConvertToLongList(selectedNoteIds);
        
        var items = new List<SpecMenuItem>();

        // Single card selected: Prioritize + Note actions
        if (cardIds.Count == 1)
        {
            items.Add(SpecMenuItem.Command("Prioritize selected cards", 
                () => OnPrioritizeCards(cardIds)));

            // Note submenu - uses existing context menu for the selected note
            var note = GetNoteFromCardId(cardIds[0]);
            if (note != null)
            {
                items.Add(BuildNoteActionsSubmenu(note));
            }
        }

        // Any cards selected: Spread submenu
        if (cardIds.Count > 0)
        {
            items.Add(BuildSpreadSubmenu(cardIds));
        }

        // Selected sentence notes: Reparse action
        var sentenceNotes = GetSentenceNotes(noteIds);
        if (sentenceNotes.Any())
        {
            items.Add(SpecMenuItem.Command("Reparse sentence words", 
                () => OnReparseSentences(sentenceNotes)));
        }

        return SpecMenuItem.Submenu("&Magnus", items);
    }

    private static SpecMenuItem BuildNoteActionsSubmenu(JPNote note)
    {
        // Build note-specific context menu using existing infrastructure
        // Just return their note actions submenu for the specific note type
        if (note is VocabNote vocab)
        {
            return VocabNoteMenus.BuildNoteActionsMenuSpec(vocab);
        }
        else if (note is KanjiNote kanji)
        {
            return KanjiNoteMenus.BuildNoteActionsMenuSpec(kanji);
        }
        else if (note is SentenceNote sentence)
        {
            return SentenceNoteMenus.BuildNoteActionsMenuSpec(sentence);
        }
        
        // Fallback: empty submenu
        return SpecMenuItem.Submenu(ShortcutFinger.Home3("Note"), new List<SpecMenuItem>());
    }

    private static SpecMenuItem BuildSpreadSubmenu(List<long> cardIds)
    {
        var startDayMenus = new List<SpecMenuItem>();

        for (int startDay = 0; startDay <= 9; startDay++)
        {
            var daysApartItems = new List<SpecMenuItem>();
            
            for (int daysApart = 1; daysApart <= 9; daysApart++)
            {
                int currentStartDay = startDay; // Capture for lambda
                int currentDaysApart = daysApart;
                
                daysApartItems.Add(SpecMenuItem.Command($"{currentDaysApart} days apart", 
                    () => OnSpreadCards(cardIds, currentStartDay, currentDaysApart)));
            }

            startDayMenus.Add(SpecMenuItem.Submenu($"First card in {startDay} days", daysApartItems));
        }

        return SpecMenuItem.Submenu("&Spread selected cards", startDayMenus);
    }

    // Action handlers
    private static void OnPrioritizeCards(List<long> cardIds)
    {
        try
        {
            AnkiFacade.PrioritizeCards(cardIds);
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to prioritize cards: {ex.Message}");
            AnkiFacade.ShowTooltip($"Failed to prioritize cards: {ex.Message}", 5000);
        }
    }

    private static void OnSpreadCards(List<long> cardIds, int startDay, int daysApart)
    {
        try
        {
            AnkiFacade.SpreadCardsOverDays(cardIds, startDay, daysApart);
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to spread cards: {ex.Message}");
            AnkiFacade.ShowTooltip($"Failed to spread cards: {ex.Message}", 5000);
        }
    }

    private static void OnReparseSentences(List<SentenceNote> sentences)
    {
        try
        {
            Core.TemporaryServiceCollection.Instance.LocalNoteUpdater.ReparseSentences(sentences, runGcDuringBatch: true);
            AnkiFacade.Refresh();
            AnkiFacade.ShowTooltip($"Reparsed {sentences.Count} sentence(s)", 3000);
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to reparse sentences: {ex.Message}");
            AnkiFacade.ShowTooltip($"Failed to reparse sentences: {ex.Message}", 5000);
        }
    }

    // Helper methods
    private static List<long> ConvertToLongList(dynamic pythonList)
    {
        if (pythonList == null) return new List<long>();
        
        try
        {
            var result = new List<long>();
            foreach (var item in pythonList)
            {
                result.Add(Convert.ToInt64(item));
            }
            return result;
        }
        catch
        {
            return new List<long>();
        }
    }

    private static JPNote? GetNoteFromCardId(long cardId)
    {
        try
        {
            // Get note ID from card ID via AnkiFacade, then load from collection
            var noteId = AnkiFacade.GetNoteIdFromCardId(cardId);
            
            // Try each note type collection
            var vocab = Core.TemporaryServiceCollection.Instance.App.Col().Vocab.WithIdOrNone((int)noteId);
            if (vocab != null) return vocab;
            
            var sentence = Core.TemporaryServiceCollection.Instance.App.Col().Sentences.WithIdOrNone((int)noteId);
            if (sentence != null) return sentence;
            
            var kanji = Core.TemporaryServiceCollection.Instance.App.Col().Kanji.WithIdOrNone((int)noteId);
            return kanji;
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to get note from card ID {cardId}: {ex.Message}");
            return null;
        }
    }

    private static List<SentenceNote> GetSentenceNotes(List<long> noteIds)
    {
        var sentences = new List<SentenceNote>();
        
        foreach (var noteId in noteIds)
        {
            try
            {
                var note = Core.TemporaryServiceCollection.Instance.App.Col().Sentences.WithIdOrNone((int)noteId);
                if (note != null)
                {
                    sentences.Add(note);
                }
            }
            catch (Exception ex)
            {
                JALogger.Log($"Failed to load note {noteId}: {ex.Message}");
            }
        }

        return sentences;
    }
}
