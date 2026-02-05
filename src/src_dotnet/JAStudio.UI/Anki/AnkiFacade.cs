using System;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.UI.Anki;

/// <summary>
/// Facade for calling Anki functionality from C#.
/// Uses Python.NET to invoke Python code in the Anki environment.
/// This isolates all pythonnet interop in one place, following the same pattern as JNTokenizer.
/// </summary>
public static class AnkiFacade
{
    /// <summary>
    /// Execute an Anki browser search query.
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
    /// Refresh the current note's generated data.
    /// Equivalent to: jastudio.ui.tools_menu.refresh()
    /// </summary>
    public static void Refresh()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic toolsMenu = Py.Import("jastudio.ui.tools_menu");
                toolsMenu.refresh();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.Refresh failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Open a URL in the default browser.
    /// Equivalent to: webbrowser.open(url)
    /// </summary>
    public static void OpenUrl(string url)
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic webbrowser = Py.Import("webbrowser");
                webbrowser.open(url);
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.OpenUrl failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Show a tooltip message in Anki.
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
    /// Run a UI action with error handling and busy cursor.
    /// Equivalent to: jastudio.ankiutils.app.get_ui_utils().run_ui_action(action)
    /// Note: Calling C# actions from Python is complex, best to avoid this for now.
    /// </summary>
    public static void RunUiAction(Action action)
    {
        // TODO: Implement this if needed - requires creating Python callable from C# Action
        // For now, just execute the action directly
        action();
    }

    /// <summary>
    /// Show the note search dialog.
    /// Equivalent to: jastudio.ui.open_note.open_note_dialog.NoteSearchDialog.toggle_dialog_visibility()
    /// </summary>
    public static void ShowNoteSearchDialog()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic openNoteDialog = Py.Import("jastudio.ui.open_note.open_note_dialog");
                openNoteDialog.NoteSearchDialog.toggle_dialog_visibility();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.ShowNoteSearchDialog failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Show the readings mappings dialog.
    /// Equivalent to: jastudio.configuration.readings_mapping_dialog.show_readings_mappings()
    /// </summary>
    public static void ShowReadingsMappingsDialog()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic readingsMappingDialog = Py.Import("jastudio.configuration.readings_mapping_dialog");
                readingsMappingDialog.show_readings_mappings();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.ShowReadingsMappingsDialog failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Convert Immersion Kit sentences.
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

    /// <summary>
    /// Update all notes (vocab, kanji, sentences, metadata).
    /// Equivalent to: jastudio.batches.local_note_updater.update_all()
    /// </summary>
    public static void UpdateAll()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic updater = Py.Import("jastudio.batches.local_note_updater");
                updater.update_all();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.UpdateAll failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Update vocabulary notes.
    /// Equivalent to: jastudio.batches.local_note_updater.update_vocab()
    /// </summary>
    public static void UpdateVocab()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic updater = Py.Import("jastudio.batches.local_note_updater");
                updater.update_vocab();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.UpdateVocab failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Update kanji notes.
    /// Equivalent to: jastudio.batches.local_note_updater.update_kanji()
    /// </summary>
    public static void UpdateKanji()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic updater = Py.Import("jastudio.batches.local_note_updater");
                updater.update_kanji();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.UpdateKanji failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Update sentence notes.
    /// Equivalent to: jastudio.batches.local_note_updater.update_sentences()
    /// </summary>
    public static void UpdateSentences()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic updater = Py.Import("jastudio.batches.local_note_updater");
                updater.update_sentences();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.UpdateSentences failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Tag note metadata.
    /// Equivalent to: jastudio.batches.local_note_updater.tag_note_metadata()
    /// </summary>
    public static void TagNoteMetadata()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic updater = Py.Import("jastudio.batches.local_note_updater");
                updater.tag_note_metadata();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.TagNoteMetadata failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Reparse all sentences.
    /// Equivalent to: jastudio.batches.local_note_updater.reparse_all_sentences()
    /// </summary>
    public static void ReparseAllSentences()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic updater = Py.Import("jastudio.batches.local_note_updater");
                updater.reparse_all_sentences();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.ReparseAllSentences failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Full rebuild of all notes.
    /// Equivalent to: jastudio.batches.local_note_updater.full_rebuild()
    /// </summary>
    public static void FullRebuild()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic updater = Py.Import("jastudio.batches.local_note_updater");
                updater.full_rebuild();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.FullRebuild failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Create missing vocab notes.
    /// Equivalent to: jastudio.batches.local_note_updater.create_missing_vocab_with_dictionary_entries()
    /// </summary>
    public static void CreateMissingVocab()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic updater = Py.Import("jastudio.batches.local_note_updater");
                updater.create_missing_vocab_with_dictionary_entries();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.CreateMissingVocab failed: {ex.Message}");
                throw;
            }
        });
    }

    /// <summary>
    /// Regenerate vocab answers from Jamdict.
    /// Equivalent to: jastudio.batches.local_note_updater.regenerate_jamdict_vocab_answers()
    /// </summary>
    public static void RegenerateVocabAnswers()
    {
        PythonEnvironment.Use(() =>
        {
            try
            {
                dynamic updater = Py.Import("jastudio.batches.local_note_updater");
                updater.regenerate_jamdict_vocab_answers();
            }
            catch (Exception ex)
            {
                JALogger.Log($"AnkiFacade.RegenerateVocabAnswers failed: {ex.Message}");
                throw;
            }
        });
    }
}
