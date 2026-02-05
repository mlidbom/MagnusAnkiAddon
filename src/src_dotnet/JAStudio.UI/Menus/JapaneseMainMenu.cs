using System;
using System.Collections.Generic;
using Avalonia.Controls;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds the main "Japanese" menu for Anki.
/// This will replace the Python menu in tools_menu.py.
/// </summary>
public class JapaneseMainMenu
{
    private readonly Action _refreshCallback;

    public JapaneseMainMenu(Action refreshCallback)
    {
        _refreshCallback = refreshCallback;
    }

    /// <summary>
    /// Build the complete Japanese main menu structure.
    /// </summary>
    public List<MenuItem> BuildMenu()
    {
        return new List<MenuItem>
        {
            BuildConfigMenu(),
            BuildLookupMenu(),
            BuildLocalActionsMenu(),
            BuildDebugMenu()
        };
    }

    private MenuItem BuildConfigMenu()
    {
        var menuItems = new List<MenuItem>
        {
            CreateMenuItem("Options (Ctrl+Shift+S)", OnOptions),
            CreateMenuItem("Readings mappings (Ctrl+Shift+M)", OnReadingsMappings)
        };

        return new MenuItem
        {
            Header = "Config",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildLookupMenu()
    {
        var menuItems = new List<MenuItem>
        {
            CreateMenuItem("Open note (Ctrl+O)", OnOpenNote),
            BuildOpenInAnkiSubmenu(),
            BuildWebSearchSubmenu()
        };

        return new MenuItem
        {
            Header = "Lookup",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildLocalActionsMenu()
    {
        var menuItems = new List<MenuItem>
        {
            BuildUpdateSubmenu(),
            CreateMenuItem("Convert Immersion Kit sentences", OnConvertImmersionKitSentences),
            CreateMenuItem("Update everything except reparsing sentences", OnUpdateAll),
            CreateMenuItem("Create vocab notes for parsed words", OnCreateMissingVocab),
            CreateMenuItem("Regenerate vocab source answers from jamdict", OnRegenerateVocabAnswers)
        };

        return new MenuItem
        {
            Header = "Local Actions",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildDebugMenu()
    {
        var menuItems = new List<MenuItem>
        {
            CreateMenuItem("Show instance report", OnShowInstanceReport),
            CreateMenuItem("Take Snapshot", OnTakeSnapshot),
            CreateMenuItem("Show current snapshot diff", OnShowCurrentSnapshotDiff),
            CreateMenuItem("Show diff against first snapshot", OnShowDiffAgainstFirst),
            CreateMenuItem("Show diff against current snapshot", OnShowDiffAgainstCurrent),
            CreateMenuItem("Run GC and report", OnRunGC),
            CreateMenuItem("Reset", OnReset),
            CreateMenuItem("Refresh UI (F5)", _refreshCallback)
        };

        return new MenuItem
        {
            Header = "Debug",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildUpdateSubmenu()
    {
        var menuItems = new List<MenuItem>
        {
            CreateMenuItem("Vocab", OnUpdateVocab),
            CreateMenuItem("Kanji", OnUpdateKanji),
            CreateMenuItem("Sentences", OnUpdateSentences),
            CreateMenuItem("Tag note metadata", OnTagNoteMetadata),
            CreateMenuItem("All the above", OnUpdateAll),
            CreateMenuItem("Reparse sentences", OnReparseSentences),
            CreateMenuItem("All the above: Full rebuild", OnFullRebuild)
        };

        return new MenuItem
        {
            Header = "Update",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildOpenInAnkiSubmenu()
    {
        // TODO: Port from build_open_in_anki_menu
        return new MenuItem { Header = "Anki (TODO)" };
    }

    private MenuItem BuildWebSearchSubmenu()
    {
        // TODO: Port from build_web_search_menu
        return new MenuItem { Header = "Web (TODO)" };
    }

    private MenuItem CreateMenuItem(string header, Action onClick)
    {
        var item = new MenuItem { Header = header };
        item.Click += (s, e) => onClick();
        return item;
    }

    // Config menu actions
    private void OnOptions() => JALogger.Log("TODO: Show Japanese options dialog");
    private void OnReadingsMappings() => JALogger.Log("TODO: Show readings mappings dialog");

    // Lookup menu actions
    private void OnOpenNote() => JALogger.Log("TODO: Open note search dialog");

    // Local Actions menu actions
    private void OnConvertImmersionKitSentences() => JALogger.Log("TODO: Convert Immersion Kit sentences");
    private void OnCreateMissingVocab() => JALogger.Log("TODO: Create missing vocab notes");
    private void OnRegenerateVocabAnswers() => JALogger.Log("TODO: Regenerate vocab answers from jamdict");

    // Update submenu actions
    private void OnUpdateVocab() => JALogger.Log("TODO: Update vocab");
    private void OnUpdateKanji() => JALogger.Log("TODO: Update kanji");
    private void OnUpdateSentences() => JALogger.Log("TODO: Update sentences");
    private void OnTagNoteMetadata() => JALogger.Log("TODO: Tag note metadata");
    private void OnUpdateAll() => JALogger.Log("TODO: Update all");
    private void OnReparseSentences() => JALogger.Log("TODO: Reparse sentences");
    private void OnFullRebuild() => JALogger.Log("TODO: Full rebuild");

    // Debug menu actions
    private void OnShowInstanceReport() => JALogger.Log("TODO: Show instance report");
    private void OnTakeSnapshot() => JALogger.Log("TODO: Take snapshot");
    private void OnShowCurrentSnapshotDiff() => JALogger.Log("TODO: Show current snapshot diff");
    private void OnShowDiffAgainstFirst() => JALogger.Log("TODO: Show diff against first snapshot");
    private void OnShowDiffAgainstCurrent() => JALogger.Log("TODO: Show diff against current snapshot");
    private void OnRunGC() => JALogger.Log("TODO: Run GC and report");
    private void OnReset() => JALogger.Log("TODO: Reset");
}
