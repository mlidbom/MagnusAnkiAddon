using System;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.UI.Anki;

/// <summary>
/// Facade for calling Anki-specific functionality that cannot be implemented in pure C#.
/// Uses Python.NET to invoke Python code in the Anki environment.
/// 
/// IMPORTANT: This should only contain operations that REQUIRE Anki's Python API.
/// All business logic should use JAStudio.Core directly.
/// All browser operations should use BrowserLauncher.OpenUrl.
/// All batch operations should use JAStudio.Core.Batches.LocalNoteUpdater.
/// </summary>
public static class AnkiFacade
{
    /// <summary>
    /// Execute an Anki browser search query.
    /// This requires Anki's browser API and cannot be implemented in pure C#.
    /// Equivalent to: jastudio.ankiutils.search_executor.do_lookup(query)
    /// </summary>
    public static void ExecuteLookup(string query)
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic searchExecutor = Py.Import("jastudio.ankiutils.search_executor");
                searchExecutor.do_lookup(query);
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.ExecuteLookup failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Show a tooltip message in Anki.
    /// This requires Anki's UI and cannot be implemented in pure C#.
    /// Equivalent to: aqt.utils.tooltip(message, period)
    /// </summary>
    public static void ShowTooltip(string message, int periodMs = 3000)
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic aqtUtils = Py.Import("aqt.utils");
                aqtUtils.tooltip(message, periodMs);
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.ShowTooltip failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Convert Immersion Kit sentences.
    /// TEMPORARY: This operation is not yet ported to C#.
    /// Equivalent to: jastudio.batches.local_note_updater.convert_immersion_kit_sentences()
    /// </summary>
    public static void ConvertImmersionKitSentences()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic updater = Py.Import("jastudio.batches.local_note_updater");
                updater.convert_immersion_kit_sentences();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.ConvertImmersionKitSentences failed: {ex.Message}");
                throw;
            }
        });
    }
}
