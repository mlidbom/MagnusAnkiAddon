using System;
using System.Collections.Generic;
using JAStudio.Core;
using JAStudio.Core.Note;
using JAStudio.UI.Anki;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;
using JAStudio.UI.Views;
using SpecMenuItem = JAStudio.UI.Menus.UIAgnosticMenuStructure.MenuItem;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds context menus for different note types and contexts.
/// This will replace the Python menu in common.py.
/// Now uses UI-agnostic MenuItem specifications and AnkiFacade for Anki calls.
/// </summary>
public class NoteContextMenu
{
    public NoteContextMenu()
    {
    }

    /// <summary>
    /// Build context menu for a vocab note as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildVocabContextMenuSpec(int vocabId, string selection, string clipboard)
    {
        var vocabCache = Core.App.Col().Vocab;
        var vocab = vocabCache.WithIdOrNone(vocabId);
        if (vocab == null)
            return new List<SpecMenuItem>();

        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, "vocab"));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, "vocab"));

        menuItems.Add(BuildVocabNoteActionsMenuSpec(vocab));
        menuItems.Add(BuildUniversalNoteActionsMenuSpec());
        menuItems.Add(BuildVocabViewMenuSpec());

        return menuItems;
    }

    /// <summary>
    /// Build context menu for a vocab note and convert to Avalonia MenuItems.
    /// </summary>
    public List<Avalonia.Controls.MenuItem> BuildVocabContextMenu(int vocabId, string selection, string clipboard)
    {
        var specs = BuildVocabContextMenuSpec(vocabId, selection, clipboard);
        var result = new List<Avalonia.Controls.MenuItem>();
        foreach (var spec in specs)
            result.Add(AvaloniaMenuAdapter.ToAvalonia(spec));
        return result;
    }

    /// <summary>
    /// Build context menu for a kanji note as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildKanjiContextMenuSpec(int kanjiId, string selection, string clipboard)
    {
        var kanjiCache = Core.App.Col().Kanji;
        var kanji = kanjiCache.WithIdOrNone(kanjiId);
        if (kanji == null)
            return new List<SpecMenuItem>();

        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, "kanji"));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, "kanji"));

        menuItems.Add(BuildKanjiNoteActionsMenuSpec());
        menuItems.Add(BuildUniversalNoteActionsMenuSpec());
        menuItems.Add(BuildKanjiViewMenuSpec());

        return menuItems;
    }

    /// <summary>
    /// Build context menu for a kanji note and convert to Avalonia MenuItems.
    /// </summary>
    public List<Avalonia.Controls.MenuItem> BuildKanjiContextMenu(int kanjiId, string selection, string clipboard)
    {
        var specs = BuildKanjiContextMenuSpec(kanjiId, selection, clipboard);
        var result = new List<Avalonia.Controls.MenuItem>();
        foreach (var spec in specs)
            result.Add(AvaloniaMenuAdapter.ToAvalonia(spec));
        return result;
    }

    /// <summary>
    /// Build context menu for a sentence note as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildSentenceContextMenuSpec(int sentenceId, string selection, string clipboard)
    {
        var sentenceCache = Core.App.Col().Sentences;
        var sentence = sentenceCache.WithIdOrNone(sentenceId);
        if (sentence == null)
            return new List<SpecMenuItem>();

        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, "sentence"));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, "sentence"));

        menuItems.Add(BuildSentenceNoteActionsMenuSpec());
        menuItems.Add(BuildUniversalNoteActionsMenuSpec());
        menuItems.Add(BuildSentenceViewMenuSpec());

        return menuItems;
    }

    /// <summary>
    /// Build context menu for a sentence note and convert to Avalonia MenuItems.
    /// </summary>
    public List<Avalonia.Controls.MenuItem> BuildSentenceContextMenu(int sentenceId, string selection, string clipboard)
    {
        var specs = BuildSentenceContextMenuSpec(sentenceId, selection, clipboard);
        var result = new List<Avalonia.Controls.MenuItem>();
        foreach (var spec in specs)
            result.Add(AvaloniaMenuAdapter.ToAvalonia(spec));
        return result;
    }

    /// <summary>
    /// Build context menu when no note is available as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildGenericContextMenuSpec(string selection, string clipboard)
    {
        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, null));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, null));

        return menuItems;
    }

    /// <summary>
    /// Build generic context menu and convert to Avalonia MenuItems.
    /// </summary>
    public List<Avalonia.Controls.MenuItem> BuildGenericContextMenu(string selection, string clipboard)
    {
        var specs = BuildGenericContextMenuSpec(selection, clipboard);
        var result = new List<Avalonia.Controls.MenuItem>();
        foreach (var spec in specs)
            result.Add(AvaloniaMenuAdapter.ToAvalonia(spec));
        return result;
    }

    private SpecMenuItem BuildSelectionMenuSpec(string selection, string? noteType)
    {
        var truncated = TruncateText(selection, 40);
        var menuItems = BuildStringMenuSpec(selection, noteType);

        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1($"Selection: \"{truncated}\""),
            menuItems
        );
    }

    private SpecMenuItem BuildClipboardMenuSpec(string clipboard, string? noteType)
    {
        var truncated = TruncateText(clipboard, 40);
        var menuItems = BuildStringMenuSpec(clipboard, noteType);

        return SpecMenuItem.Submenu(
            ShortcutFinger.Home2($"Clipboard: \"{truncated}\""),
            menuItems
        );
    }

    private List<SpecMenuItem> BuildStringMenuSpec(string text, string? noteType)
    {
        return new List<SpecMenuItem>
        {
            BuildCurrentNoteActionsSubmenuSpec(text, noteType),
            OpenInAnkiMenus.BuildOpenInAnkiMenuSpec(() => text),
            WebSearchMenus.BuildWebSearchMenuSpec(() => text),
            BuildMatchingNotesSubmenuSpec(text),
            BuildCreateNoteSubmenuSpec(text),
            SpecMenuItem.Command(ShortcutFinger.Down1($"Reparse matching sentences"), () => OnReparseMatchingSentences(text))
        };
    }

    // Vocab-specific menus
    private SpecMenuItem BuildVocabNoteActionsMenuSpec(VocabNote vocab)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Note actions"),
            new List<SpecMenuItem>
            {
                SpecMenuItem.Command(ShortcutFinger.Home2("Edit flags"), () => OnEditVocabFlags(vocab)),
                SpecMenuItem.Command("Vocab Actions (TODO)", () => { })
            }
        );
    }

    private SpecMenuItem BuildVocabViewMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home5("View"),
            new List<SpecMenuItem>
            {
                // TODO: Port from menus.notes.vocab.main.build_view_menu
                SpecMenuItem.Command("View Vocab (TODO)", () => { })
            }
        );
    }

    // Kanji-specific menus
    private SpecMenuItem BuildKanjiNoteActionsMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Note actions"),
            new List<SpecMenuItem>
            {
                // TODO: Port from menus.notes.kanji.main.build_note_menu
                SpecMenuItem.Command("Kanji Actions (TODO)", () => { })
            }
        );
    }

    private SpecMenuItem BuildKanjiViewMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home5("View"),
            new List<SpecMenuItem>
            {
                // TODO: Port from menus.notes.kanji.main.build_view_menu
                SpecMenuItem.Command("View Kanji (TODO)", () => { })
            }
        );
    }

    // Sentence-specific menus
    private SpecMenuItem BuildSentenceNoteActionsMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Note actions"),
            new List<SpecMenuItem>
            {
                // TODO: Port from menus.notes.sentence.main.build_note_menu
                SpecMenuItem.Command("Sentence Actions (TODO)", () => { })
            }
        );
    }

    private SpecMenuItem BuildSentenceViewMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home5("View"),
            new List<SpecMenuItem>
            {
                // TODO: Port from menus.notes.sentence.main.build_view_menu
                SpecMenuItem.Command("View Sentence (TODO)", () => { })
            }
        );
    }

    private SpecMenuItem BuildUniversalNoteActionsMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home4("Universal note actions"),
            new List<SpecMenuItem>
            {
                SpecMenuItem.Command(ShortcutFinger.Home1("Open in previewer"), OnOpenInPreviewer),
                SpecMenuItem.Command(ShortcutFinger.Home3("Unsuspend all cards"), OnUnsuspendAllCards),
                SpecMenuItem.Command(ShortcutFinger.Home4("Suspend all cards"), OnSuspendAllCards)
            }
        );
    }

    private SpecMenuItem BuildCurrentNoteActionsSubmenuSpec(string text, string? noteType)
    {
        // TODO: Port string_note_menu_factory logic
        return SpecMenuItem.Submenu(ShortcutFinger.Home1("Current note actions (TODO)"), new List<SpecMenuItem>());
    }

    private SpecMenuItem BuildMatchingNotesSubmenuSpec(string text)
    {
        // TODO: Port from build_matching_note_menu
        return SpecMenuItem.Submenu(ShortcutFinger.Home4("Exactly matching notes (TODO)"), new List<SpecMenuItem>());
    }

    private SpecMenuItem BuildCreateNoteSubmenuSpec(string text)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Up1($"Create: {TruncateText(text, 40)}"),
            new List<SpecMenuItem>
            {
                SpecMenuItem.Command(ShortcutFinger.Home1("vocab"), () => OnCreateVocabNote(text)),
                SpecMenuItem.Command(ShortcutFinger.Home2("sentence"), () => OnCreateSentenceNote(text)),
                SpecMenuItem.Command(ShortcutFinger.Home3("kanji"), () => OnCreateKanjiNote(text))
            }
        );
    }

    private static string TruncateText(string text, int maxLength)
    {
        if (text.Length <= maxLength)
            return text;
        return text.Substring(0, maxLength) + "...";
    }

    // Action handlers
    private void OnEditVocabFlags(VocabNote vocab)
    {
        var dialog = new VocabFlagsDialog(vocab);
        dialog.Show();
    }
    
    private void OnReparseMatchingSentences(string text) => JALogger.Log($"TODO: Reparse matching sentences: {text}");
    private void OnOpenInPreviewer() => JALogger.Log("TODO: Open in previewer");
    private void OnUnsuspendAllCards() => JALogger.Log("TODO: Unsuspend all cards");
    private void OnSuspendAllCards() => JALogger.Log("TODO: Suspend all cards");
    private void OnCreateVocabNote(string text) => JALogger.Log($"TODO: Create vocab note: {text}");
    private void OnCreateSentenceNote(string text) => JALogger.Log($"TODO: Create sentence note: {text}");
    private void OnCreateKanjiNote(string text) => JALogger.Log($"TODO: Create kanji note: {text}");
}
