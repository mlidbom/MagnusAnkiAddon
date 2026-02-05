using System;
using System.Collections.Generic;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;
using SpecMenuItem = JAStudio.UI.Menus.UIAgnosticMenuStructure.MenuItem;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds the main "Japanese" menu for Anki.
/// This will replace the Python menu in tools_menu.py.
/// Now uses UI-agnostic MenuItem specifications.
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
    /// Build the complete Japanese main menu structure as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildMenuSpec()
    {
        return new List<SpecMenuItem>
        {
            BuildConfigMenuSpec(),
            BuildLookupMenuSpec(),
            BuildLocalActionsMenuSpec()
            // Note: Debug menu excluded from C# port - Python runtime diagnostics remain in Python menu
        };
    }

    /// <summary>
    /// Build the menu and convert to Avalonia MenuItems.
    /// This is a convenience method for backward compatibility.
    /// </summary>
    public List<Avalonia.Controls.MenuItem> BuildMenu()
    {
        var specs = BuildMenuSpec();
        var result = new List<Avalonia.Controls.MenuItem>();
        foreach (var spec in specs)
        {
            result.Add(AvaloniaMenuAdapter.ToAvalonia(spec));
        }
        return result;
    }

    private SpecMenuItem BuildConfigMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1("Config"),
            new List<SpecMenuItem>
            {
                SpecMenuItem.Command(ShortcutFinger.Home1("Options (Ctrl+Shift+S)"), OnOptions),
                SpecMenuItem.Command(ShortcutFinger.Home2("Readings mappings (Ctrl+Shift+M)"), OnReadingsMappings)
            }
        );
    }

    private SpecMenuItem BuildLookupMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home2("Lookup"),
            new List<SpecMenuItem>
            {
                SpecMenuItem.Command(ShortcutFinger.Home1("Open note (Ctrl+O)"), OnOpenNote),
                OpenInAnkiMenus.BuildOpenInAnkiMenuSpec(() => _searchText, _executeLookup),
                WebSearchMenus.BuildWebSearchMenuSpec(() => _searchText, BrowserLauncher.OpenUrl)
            }
        );
    }

    private SpecMenuItem BuildLocalActionsMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Local Actions"),
            new List<SpecMenuItem>
            {
                BuildUpdateSubmenuSpec(),
                SpecMenuItem.Command(ShortcutFinger.Home2("Convert Immersion Kit sentences"), OnConvertImmersionKitSentences),
                SpecMenuItem.Command(ShortcutFinger.Home3("Update everything except reparsing sentences"), OnUpdateAll),
                SpecMenuItem.Command(ShortcutFinger.Home4("Create vocab notes for parsed words"), OnCreateMissingVocab),
                SpecMenuItem.Command(ShortcutFinger.Home5("Regenerate vocab source answers from jamdict"), OnRegenerateVocabAnswers)
            }
        );
    }

    private SpecMenuItem BuildUpdateSubmenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1("Update"),
            new List<SpecMenuItem>
            {
                SpecMenuItem.Command(ShortcutFinger.Home1("Vocab"), OnUpdateVocab),
                SpecMenuItem.Command(ShortcutFinger.Home2("Kanji"), OnUpdateKanji),
                SpecMenuItem.Command(ShortcutFinger.Home3("Sentences"), OnUpdateSentences),
                SpecMenuItem.Command(ShortcutFinger.Home4("Tag note metadata"), OnTagNoteMetadata),
                SpecMenuItem.Command(ShortcutFinger.Home5("All the above"), OnUpdateAll),
                SpecMenuItem.Command(ShortcutFinger.Up1("Reparse sentences"), OnReparseSentences),
                SpecMenuItem.Command(ShortcutFinger.Down1("All the above: Full rebuild"), OnFullRebuild)
            }
        );
    }

    // Config menu actions
    private void OnOptions()
    {
        JALogger.Log("OnOptions() called!");
        JALogger.Log("Calling DialogHost.ShowOptionsDialog()...");
        DialogHost.ShowOptionsDialog();
        JALogger.Log("DialogHost.ShowOptionsDialog() completed");
    }
    
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
}
