using JAStudio.PythonInterop;
using JAStudio.PythonInterop.Utilities;

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
   static readonly PythonObjectWrapper SearchExecutor = PythonEnvironment.Import("jastudio.ankiutils.search_executor");
   static readonly PythonObjectWrapper AqtUtils = PythonEnvironment.Import("aqt.utils");
   static readonly PythonObjectWrapper App = PythonEnvironment.Import("jastudio.ankiutils.app");
   static readonly PythonObjectWrapper LocalNoteUpdater = PythonEnvironment.Import("jastudio.batches.local_note_updater");
   static readonly PythonObjectWrapper QueueManager = PythonEnvironment.Import("jastudio.note.queue_manager");
   static readonly PythonObjectWrapper BrowserMain = PythonEnvironment.Import("jastudio.ui.menus.browser.main");
   static readonly PythonObjectWrapper NoteExModule = PythonEnvironment.Import("jastudio.anki_extentions.note_ex");
   static readonly PythonObjectWrapper Aqt = PythonEnvironment.Import("aqt");

   public static class Browser
   {
      /// <summary>Execute an Anki browser search query. </summary>
      public static void ExecuteLookup(string query) => SearchExecutor.Use(it => it.do_lookup(query));

      /// <summary>Execute an Anki browser search query and show the previewer. </summary>
      public static void ExecuteLookupAndShowPreviewer(string query) => SearchExecutor.Use(it => it.do_lookup_and_show_previewer(query));

      public static class MenuActions
      {
         /// <summary>Prioritize selected cards (sets card.due based on note type priority).</summary>
         public static void PrioritizeCards(System.Collections.Generic.List<long> cardIds) => QueueManager.Use(it => it.prioritize_selected_cards(PythonDotNetShim.LongList.ToPython(cardIds)));

         /// <summary>Spread selected cards over days (distributes due dates across time range).</summary>
         public static void SpreadCardsOverDays(System.Collections.Generic.List<long> cardIds, int startDay, int daysApart) => BrowserMain.Use(it => it.spread_due_dates(PythonDotNetShim.LongList.ToPython(cardIds), startDay, daysApart));
      }
   }

   public static class UIUtils
   {
      /// <summary>Show a tooltip message in Anki. </summary>
      public static void ShowTooltip(string message, int periodMs = 3000) => AqtUtils.Use(it => it.tooltip(message, periodMs));

      /// <summary>Refresh the currently displayed views in Anki. By it's nature it cannot be ported. </summary>
      public static void Refresh() => App.Use(it => it.get_ui_utils().refresh());
   }

   public static class Batches
   {
      /// <summary>This is about converting between Anki note types. There's no way to avoid interfacing with anki for that. </summary>
      public static void ConvertImmersionKitSentences() => LocalNoteUpdater.Use(it => it.convert_immersion_kit_sentences());
   }

   public static class NoteEx
   {
      /// <summary>Suspend all cards for the given note ID.</summary>
      public static void SuspendAllCardsForNote(long noteId) => NoteExModule.Use(it => it.NoteEx.from_id(noteId).suspend_all_cards());

      /// <summary>Unsuspend all cards for the given note ID.</summary>
      public static void UnsuspendAllCardsForNote(long noteId) => NoteExModule.Use(it => it.NoteEx.from_id(noteId).un_suspend_all_cards());
   }

   public static class Col
   {
      public static string DbFilePath() => Aqt.Use(it => (string)it.mw.col.path);
   }

   /// <summary>Get note ID from card ID (requires Anki API).</summary>
   public static long GetNoteIdFromCardId(long cardId) => App.Use(it => (long)it.anki_collection().get_card(cardId).nid);

   

}
