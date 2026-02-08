using System;
using System.Collections.Generic;
using JAStudio.Core.Anki;
using JAStudio.Core.Note;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds browser context menu for Anki's card browser.
/// Corresponds to ui/menus/browser/main.py in Python.
/// </summary>
public class BrowserMenus
{
   readonly Core.TemporaryServiceCollection _services;
   readonly VocabNoteMenus _vocabNoteMenus;
   readonly KanjiNoteMenus _kanjiNoteMenus;
   readonly SentenceNoteMenus _sentenceNoteMenus;

   public BrowserMenus(Core.TemporaryServiceCollection services)
   {
      _services = services;
      _vocabNoteMenus = new VocabNoteMenus(services);
      _kanjiNoteMenus = new KanjiNoteMenus(services);
      _sentenceNoteMenus = new SentenceNoteMenus(services);
   }

   /// <summary>
   /// Build the complete browser context menu structure as UI-agnostic specifications.
   /// </summary>
   /// <param name="selectedCardIds">List of selected card IDs (from Python/Anki)</param>
   /// <param name="selectedNoteIds">List of selected note IDs (from Python/Anki)</param>
   public SpecMenuItem BuildBrowserMenuSpec(dynamic selectedCardIds, dynamic selectedNoteIds)
   {
      var cardIds = ConvertToLongList(selectedCardIds);
      var noteIds = ConvertToLongList(selectedNoteIds);

      var items = new List<SpecMenuItem>();

      // Single card selected: Prioritize + Note actions
      if(cardIds.Count == 1)
      {
         items.Add(SpecMenuItem.Command("Prioritize selected cards",
                                        () => OnPrioritizeCards(cardIds)));

         // Note submenu - uses existing context menu for the selected note
         var note = GetNoteFromCardId(cardIds[0]);
         if(note != null)
         {
            items.Add(BuildNoteActionsSubmenu(note));
         }
      }

      // Any cards selected: Spread submenu
      if(cardIds.Count > 0)
      {
         items.Add(BuildSpreadSubmenu(cardIds));
      }

      // Selected sentence notes: Reparse action
      var sentenceNotes = GetSentenceNotes(noteIds);
      if(sentenceNotes.Any())
      {
         items.Add(SpecMenuItem.Command("Reparse sentence words",
                                        () => OnReparseSentences(sentenceNotes)));
      }

      return SpecMenuItem.Submenu("&Magnus", items);
   }

   private SpecMenuItem BuildNoteActionsSubmenu(JPNote note)
   {
      // Build note-specific context menu using existing infrastructure
      // Just return their note actions submenu for the specific note type
      if(note is VocabNote vocab)
      {
         return _vocabNoteMenus.BuildNoteActionsMenuSpec(vocab);
      } else if(note is KanjiNote kanji)
      {
         return _kanjiNoteMenus.BuildNoteActionsMenuSpec(kanji);
      } else if(note is SentenceNote sentence)
      {
         return _sentenceNoteMenus.BuildNoteActionsMenuSpec(sentence);
      }

      // Fallback: empty submenu
      return SpecMenuItem.Submenu(ShortcutFinger.Home3("Note"), new List<SpecMenuItem>());
   }

   private static SpecMenuItem BuildSpreadSubmenu(List<long> cardIds)
   {
      var startDayMenus = new List<SpecMenuItem>();

      for(int startDay = 0; startDay <= 9; startDay++)
      {
         var daysApartItems = new List<SpecMenuItem>();

         for(int daysApart = 1; daysApart <= 9; daysApart++)
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
   private static void OnPrioritizeCards(List<long> cardIds) => AnkiFacade.Browser.MenuActions.PrioritizeCards(cardIds);

   private static void OnSpreadCards(List<long> cardIds, int startDay, int daysApart) => AnkiFacade.Browser.MenuActions.SpreadCardsOverDays(cardIds, startDay, daysApart);

   private void OnReparseSentences(List<SentenceNote> sentences)
   {
      _services.LocalNoteUpdater.ReparseSentences(sentences);
      AnkiFacade.UIUtils.Refresh();
      AnkiFacade.UIUtils.ShowTooltip($"Reparsed {sentences.Count} sentence(s)", 3000);
   }

   // Helper methods
   private static List<long> ConvertToLongList(dynamic pythonList)
   {
      if(pythonList == null) return new List<long>();

      var result = new List<long>();
      foreach(var item in pythonList)
      {
         result.Add(Convert.ToInt64(item));
      }

      return result;
   }

   private JPNote? GetNoteFromCardId(long cardId)
   {
      try
      {
         // Get Anki note ID from card ID via AnkiFacade, then look up by Anki ID
         var ankiNoteId = AnkiFacade.GetNoteIdFromCardId(cardId);

         // Try each note type collection using Anki ID mapping
         JPNote? vocab = _services.App.Collection.Vocab.WithAnkiIdOrNone(ankiNoteId);
         if(vocab != null) return vocab;

         JPNote? sentence = _services.App.Collection.Sentences.WithAnkiIdOrNone(ankiNoteId);
         if(sentence != null) return sentence;

         JPNote? kanji = _services.App.Collection.Kanji.WithAnkiIdOrNone(ankiNoteId);
         return kanji;
      }
      catch(Exception ex)
      {
         JALogger.Log($"Failed to get note from card ID {cardId}: {ex.Message}");
         return null;
      }
   }

   private List<SentenceNote> GetSentenceNotes(List<long> ankiNoteIds)
   {
      var sentences = new List<SentenceNote>();

      foreach(var ankiNoteId in ankiNoteIds)
      {
         try
         {
            var note = _services.App.Collection.Sentences.WithAnkiIdOrNone(ankiNoteId) as SentenceNote;
            if(note != null)
            {
               sentences.Add(note);
            }
         }
         catch(Exception ex)
         {
            JALogger.Log($"Failed to load note {ankiNoteId}: {ex.Message}");
         }
      }

      return sentences;
   }
}
