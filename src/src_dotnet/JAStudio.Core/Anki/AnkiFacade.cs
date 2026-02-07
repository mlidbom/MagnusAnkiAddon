using System;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.Core.Anki;

/// <summary>
/// Facade for calling Anki-specific functionality that cannot be implemented in pure C#.
/// Uses Python.NET to invoke Python code in the Anki environment.
/// 
/// IMPORTANT: This should only contain operations that REQUIRE Anki's Python API.
/// Anything that we can implement in C# and Avalonia should be.
/// </summary>
public static class AnkiFacade
{
   /// <summary>Execute an Anki browser search query. </summary>
   public static void ExecuteLookup(string query) => PythonEnvironment.Use(() =>
   {
      dynamic searchExecutor = Py.Import("jastudio.ankiutils.search_executor");
      searchExecutor.do_lookup(query);
   });

   /// <summary>Execute an Anki browser search query and show the previewer. </summary>
   public static void ExecuteLookupAndShowPreviewer(string query) => PythonEnvironment.Use(() =>
   {
      dynamic searchExecutor = Py.Import("jastudio.ankiutils.search_executor");
      searchExecutor.do_lookup_and_show_previewer(query);
   });

   /// <summary>Show a tooltip message in Anki. </summary>
   public static void ShowTooltip(string message, int periodMs = 3000) => PythonEnvironment.Use(() =>
   {
      dynamic aqtUtils = Py.Import("aqt.utils");
      aqtUtils.tooltip(message, periodMs);
   });

   /// <summary>Refresh the currently displayed views in Anki. By it's nature it cannot be ported. </summary>
   public static void Refresh() => PythonEnvironment.Use(() =>
   {
      dynamic app = Py.Import("jastudio.ankiutils.app");
      dynamic uiUtils = app.get_ui_utils();
      uiUtils.refresh();
   });

   /// <summary>This is about converting between Anki note types. There's no way to avoid interfacing with anki for that. </summary>
   public static void ConvertImmersionKitSentences() => PythonEnvironment.Use(() =>
   {
      dynamic updater = Py.Import("jastudio.batches.local_note_updater");
      updater.convert_immersion_kit_sentences();
   });

   /// <summary>Prioritize selected cards (sets card.due based on note type priority).</summary>
   public static void PrioritizeCards(System.Collections.Generic.List<long> cardIds) => PythonEnvironment.Use(() =>
   {
      dynamic queueManager = Py.Import("jastudio.note.queue_manager");
      dynamic pyCardIds = ToPythonList(cardIds);
      queueManager.prioritize_selected_cards(pyCardIds);
   });

   /// <summary>Spread selected cards over days (distributes due dates across time range).</summary>
   public static void SpreadCardsOverDays(System.Collections.Generic.List<long> cardIds, int startDay, int daysApart) => PythonEnvironment.Use(() =>
   {
      // Import the spread_due_dates function from browser.main
      dynamic browserMain = Py.Import("jastudio.ui.menus.browser.main");
      dynamic pyCardIds = ToPythonList(cardIds);
      browserMain.spread_due_dates(pyCardIds, startDay, daysApart);
   });

   /// <summary>Get note ID from card ID (requires Anki API).</summary>
   public static long GetNoteIdFromCardId(long cardId) => PythonEnvironment.Use(() =>
   {
      dynamic app = Py.Import("jastudio.ankiutils.app");
      dynamic ankiCol = app.anki_collection();
      dynamic card = ankiCol.get_card(cardId);
      return (long)card.nid;
   });

   /// <summary>Suspend all cards for the given note ID.</summary>
   public static void SuspendAllCardsForNote(int noteId) => PythonEnvironment.Use(() =>
   {
      dynamic noteEx = Py.Import("jastudio.anki_extentions.note_ex");
      dynamic note = noteEx.NoteEx.from_id(noteId);
      note.suspend_all_cards();
   });

   /// <summary>Unsuspend all cards for the given note ID.</summary>
   public static void UnsuspendAllCardsForNote(int noteId) => PythonEnvironment.Use(() =>
   {
      dynamic noteEx = Py.Import("jastudio.anki_extentions.note_ex");
      dynamic note = noteEx.NoteEx.from_id(noteId);
      note.un_suspend_all_cards();
   });

   /// <summary>Helper to convert C# list to Python list.</summary>
   private static dynamic ToPythonList(System.Collections.Generic.List<long> items)
   {
      using(Py.GIL())
      {
         dynamic pyList = new Python.Runtime.PyList();
         foreach(var item in items)
         {
            pyList.append(item);
         }

         return pyList;
      }
   }
}
