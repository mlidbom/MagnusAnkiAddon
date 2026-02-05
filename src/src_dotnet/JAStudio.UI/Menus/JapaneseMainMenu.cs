using System;
using System.Collections.Generic;
using Avalonia.Controls;
using JAStudio.UI.Utils;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds the main "Japanese" menu for Anki.
/// This will replace the Python menu in tools_menu.py.
/// </summary>
public class JapaneseMainMenu
{
    private readonly Action _refreshCallback;
    private readonly Action<string> _executeLookup;
    private readonly string _searchText;

    public JapaneseMainMenu(
        Action refreshCallback, 
        Action<string> executeLookup,
        string searchText)
    {
        _refreshCallback = refreshCallback;
        _executeLookup = executeLookup;
        _searchText = searchText;
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
            CreateMenuItem(ShortcutFinger.Home1("Options (Ctrl+Shift+S)"), OnOptions),
            CreateMenuItem(ShortcutFinger.Home2("Readings mappings (Ctrl+Shift+M)"), OnReadingsMappings)
        };

        return new MenuItem
        {
            Header = ShortcutFinger.Home1("Config"),
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildLookupMenu()
    {
        var menuItems = new List<MenuItem>
        {
            CreateMenuItem(ShortcutFinger.Home1("Open note (Ctrl+O)"), OnOpenNote),
            OpenInAnkiMenus.BuildOpenInAnkiMenu(() => _searchText, _executeLookup),
            WebSearchMenus.BuildWebSearchMenu(() => _searchText, BrowserLauncher.OpenUrl)
        };

        return new MenuItem
        {
            Header = ShortcutFinger.Home2("Lookup"),
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildLocalActionsMenu()
    {
        var menuItems = new List<MenuItem>
        {
            BuildUpdateSubmenu(),
            CreateMenuItem(ShortcutFinger.Home2("Convert Immersion Kit sentences"), OnConvertImmersionKitSentences),
            CreateMenuItem(ShortcutFinger.Home3("Update everything except reparsing sentences"), OnUpdateAll),
            CreateMenuItem(ShortcutFinger.Home4("Create vocab notes for parsed words"), OnCreateMissingVocab),
            CreateMenuItem(ShortcutFinger.Home5("Regenerate vocab source answers from jamdict"), OnRegenerateVocabAnswers)
        };

        return new MenuItem
        {
            Header = ShortcutFinger.Home3("Local Actions"),
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildDebugMenu()
    {
        var menuItems = new List<MenuItem>
        {
            CreateMenuItem(ShortcutFinger.Home1("Show instance report"), OnShowInstanceReport),
            CreateMenuItem(ShortcutFinger.Home2("Take Snapshot"), OnTakeSnapshot),
            CreateMenuItem(ShortcutFinger.Home3("Show current snapshot diff"), OnShowCurrentSnapshotDiff),
            CreateMenuItem(ShortcutFinger.Home4("Show diff against first snapshot"), OnShowDiffAgainstFirst),
            CreateMenuItem(ShortcutFinger.Home5("Show diff against current snapshot"), OnShowDiffAgainstCurrent),
            CreateMenuItem(ShortcutFinger.Up1("Run GC and report"), OnRunGC),
            CreateMenuItem(ShortcutFinger.Up2("Reset"), OnReset),
            CreateMenuItem(ShortcutFinger.Down1("Refresh UI (F5)"), _refreshCallback)
        };

        return new MenuItem
        {
            Header = ShortcutFinger.Home4("Debug"),
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildUpdateSubmenu()
    {
        var menuItems = new List<MenuItem>
        {
            CreateMenuItem(ShortcutFinger.Home1("Vocab"), OnUpdateVocab),
            CreateMenuItem(ShortcutFinger.Home2("Kanji"), OnUpdateKanji),
            CreateMenuItem(ShortcutFinger.Home3("Sentences"), OnUpdateSentences),
            CreateMenuItem(ShortcutFinger.Home4("Tag note metadata"), OnTagNoteMetadata),
            CreateMenuItem(ShortcutFinger.Home5("All the above"), OnUpdateAll),
            CreateMenuItem(ShortcutFinger.Up1("Reparse sentences"), OnReparseSentences),
            CreateMenuItem(ShortcutFinger.Down1("All the above: Full rebuild"), OnFullRebuild)
        };

        return new MenuItem
        {
            Header = ShortcutFinger.Home1("Update"),
            ItemsSource = menuItems
        };
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
