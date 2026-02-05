using System;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.UI.Anki;

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
   public static void ExecuteLookup(string query)
   {
      PythonEnvironment.Use(() =>
      {
         try
         {
            dynamic searchExecutor = Py.Import("jastudio.ankiutils.search_executor");
            searchExecutor.do_lookup(query);
         }
         catch(Exception ex)
         {
            JALogger.Log($"AnkiFacade.ExecuteLookup failed: {ex.Message}");
            throw;
         }
      });
   }

   /// <summary>Show a tooltip message in Anki. </summary>
   public static void ShowTooltip(string message, int periodMs = 3000)
   {
      PythonEnvironment.Use(() =>
      {
         try
         {
            dynamic aqtUtils = Py.Import("aqt.utils");
            aqtUtils.tooltip(message, periodMs);
         }
         catch(Exception ex)
         {
            JALogger.Log($"AnkiFacade.ShowTooltip failed: {ex.Message}");
            throw;
         }
      });
   }

   /// <summary>Refresh the currently displayed views in Anki. By it's nature it cannot be ported. </summary>
   public static void Refresh()
   {
      PythonEnvironment.Use(() =>
      {
         try
         {
            dynamic app = Py.Import("jastudio.ankiutils.app");
            dynamic uiUtils = app.get_ui_utils();
            uiUtils.refresh();
         }
         catch(Exception ex)
         {
            JALogger.Log($"AnkiFacade.Refresh failed: {ex.Message}");
            throw;
         }
      });
   }

   /// <summary>This is about converting between Anki note types. There's no way to avoid interfacing with anki for that. </summary>
   public static void ConvertImmersionKitSentences()
   {
      PythonEnvironment.Use(() =>
      {
         try
         {
            dynamic updater = Py.Import("jastudio.batches.local_note_updater");
            updater.convert_immersion_kit_sentences();
         }
         catch(Exception ex)
         {
            JALogger.Log($"AnkiFacade.ConvertImmersionKitSentences failed: {ex.Message}");
            throw;
         }
      });
   }
}
