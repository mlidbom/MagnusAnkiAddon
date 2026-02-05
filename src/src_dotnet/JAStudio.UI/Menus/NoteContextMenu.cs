using System;
using System.Collections.Generic;
using Avalonia.Controls;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds context menus for different note types and contexts.
/// This will replace the Python menu in common.py.
/// </summary>
public class NoteContextMenu
{
    private readonly Action _refreshCallback;

    public NoteContextMenu(Action refreshCallback)
    {
        _refreshCallback = refreshCallback;
    }

    /// <summary>
    /// Build context menu for a vocab note.
    /// </summary>
    public List<MenuItem> BuildVocabContextMenu(string selection, string clipboard)
    {
        var menuItems = new List<MenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenu(selection, "vocab"));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenu(clipboard, "vocab"));

        menuItems.Add(BuildVocabNoteActionsMenu());
        menuItems.Add(BuildUniversalNoteActionsMenu());
        menuItems.Add(BuildVocabViewMenu());

        return menuItems;
    }

    /// <summary>
    /// Build context menu for a kanji note.
    /// </summary>
    public List<MenuItem> BuildKanjiContextMenu(string selection, string clipboard)
    {
        var menuItems = new List<MenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenu(selection, "kanji"));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenu(clipboard, "kanji"));

        menuItems.Add(BuildKanjiNoteActionsMenu());
        menuItems.Add(BuildUniversalNoteActionsMenu());
        menuItems.Add(BuildKanjiViewMenu());

        return menuItems;
    }

    /// <summary>
    /// Build context menu for a sentence note.
    /// </summary>
    public List<MenuItem> BuildSentenceContextMenu(string selection, string clipboard)
    {
        var menuItems = new List<MenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenu(selection, "sentence"));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenu(clipboard, "sentence"));

        menuItems.Add(BuildSentenceNoteActionsMenu());
        menuItems.Add(BuildUniversalNoteActionsMenu());
        menuItems.Add(BuildSentenceViewMenu());

        return menuItems;
    }

    /// <summary>
    /// Build context menu when no note is available.
    /// </summary>
    public List<MenuItem> BuildGenericContextMenu(string selection, string clipboard)
    {
        var menuItems = new List<MenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenu(selection, null));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenu(clipboard, null));

        return menuItems;
    }

    private MenuItem BuildSelectionMenu(string selection, string? noteType)
    {
        var truncated = TruncateText(selection, 40);
        var menuItems = BuildStringMenu(selection, noteType);

        return new MenuItem
        {
            Header = $"Selection: \"{truncated}\"",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildClipboardMenu(string clipboard, string? noteType)
    {
        var truncated = TruncateText(clipboard, 40);
        var menuItems = BuildStringMenu(clipboard, noteType);

        return new MenuItem
        {
            Header = $"Clipboard: \"{truncated}\"",
            ItemsSource = menuItems
        };
    }

    private List<MenuItem> BuildStringMenu(string text, string? noteType)
    {
        var menuItems = new List<MenuItem>
        {
            BuildCurrentNoteActionsSubmenu(text, noteType),
            BuildOpenInAnkiSubmenu(text),
            BuildWebSearchSubmenu(text),
            BuildMatchingNotesSubmenu(text),
            BuildCreateNoteSubmenu(text),
            CreateMenuItem($"Reparse matching sentences", () => OnReparseMatchingSentences(text))
        };

        return menuItems;
    }

    // Vocab-specific menus
    private MenuItem BuildVocabNoteActionsMenu()
    {
        var menuItems = new List<MenuItem>
        {
            // TODO: Port from menus.notes.vocab.main.setup_note_menu
            CreateMenuItem("Edit vocab flags (TODO)", () => { }),
            CreateMenuItem("Vocab Actions (TODO)", () => { })
        };

        return new MenuItem
        {
            Header = "Note actions",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildVocabViewMenu()
    {
        var menuItems = new List<MenuItem>
        {
            // TODO: Port from menus.notes.vocab.main.build_view_menu
            CreateMenuItem("View Vocab (TODO)", () => { })
        };

        return new MenuItem
        {
            Header = "View",
            ItemsSource = menuItems
        };
    }

    // Kanji-specific menus
    private MenuItem BuildKanjiNoteActionsMenu()
    {
        var menuItems = new List<MenuItem>
        {
            // TODO: Port from menus.notes.kanji.main.build_note_menu
            CreateMenuItem("Kanji Actions (TODO)", () => { })
        };

        return new MenuItem
        {
            Header = "Note actions",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildKanjiViewMenu()
    {
        var menuItems = new List<MenuItem>
        {
            // TODO: Port from menus.notes.kanji.main.build_view_menu
            CreateMenuItem("View Kanji (TODO)", () => { })
        };

        return new MenuItem
        {
            Header = "View",
            ItemsSource = menuItems
        };
    }

    // Sentence-specific menus
    private MenuItem BuildSentenceNoteActionsMenu()
    {
        var menuItems = new List<MenuItem>
        {
            // TODO: Port from menus.notes.sentence.main.build_note_menu
            CreateMenuItem("Sentence Actions (TODO)", () => { })
        };

        return new MenuItem
        {
            Header = "Note actions",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildSentenceViewMenu()
    {
        var menuItems = new List<MenuItem>
        {
            // TODO: Port from menus.notes.sentence.main.build_view_menu
            CreateMenuItem("View Sentence (TODO)", () => { })
        };

        return new MenuItem
        {
            Header = "View",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildUniversalNoteActionsMenu()
    {
        var menuItems = new List<MenuItem>
        {
            CreateMenuItem("Open in previewer", OnOpenInPreviewer),
            CreateMenuItem("Unsuspend all cards", OnUnsuspendAllCards),
            CreateMenuItem("Suspend all cards", OnSuspendAllCards)
        };

        return new MenuItem
        {
            Header = "Universal note actions",
            ItemsSource = menuItems
        };
    }

    private MenuItem BuildCurrentNoteActionsSubmenu(string text, string? noteType)
    {
        // TODO: Port string_note_menu_factory logic
        return new MenuItem { Header = "Current note actions (TODO)" };
    }

    private MenuItem BuildOpenInAnkiSubmenu(string text)
    {
        // TODO: Port from build_open_in_anki_menu
        return new MenuItem { Header = "Open in Anki (TODO)" };
    }

    private MenuItem BuildWebSearchSubmenu(string text)
    {
        // TODO: Port from build_web_search_menu
        return new MenuItem { Header = "Search Web (TODO)" };
    }

    private MenuItem BuildMatchingNotesSubmenu(string text)
    {
        // TODO: Port from build_matching_note_menu
        return new MenuItem { Header = "Exactly matching notes (TODO)" };
    }

    private MenuItem BuildCreateNoteSubmenu(string text)
    {
        var menuItems = new List<MenuItem>
        {
            CreateMenuItem("vocab", () => OnCreateVocabNote(text)),
            CreateMenuItem("sentence", () => OnCreateSentenceNote(text)),
            CreateMenuItem("kanji", () => OnCreateKanjiNote(text))
        };

        return new MenuItem
        {
            Header = $"Create: {TruncateText(text, 40)}",
            ItemsSource = menuItems
        };
    }

    private MenuItem CreateMenuItem(string header, Action onClick)
    {
        var item = new MenuItem { Header = header };
        item.Click += (s, e) => onClick();
        return item;
    }

    private static string TruncateText(string text, int maxLength)
    {
        if (text.Length <= maxLength)
            return text;
        return text.Substring(0, maxLength) + "...";
    }

    // Action handlers
    private void OnReparseMatchingSentences(string text) => JALogger.Log($"TODO: Reparse matching sentences: {text}");
    private void OnOpenInPreviewer() => JALogger.Log("TODO: Open in previewer");
    private void OnUnsuspendAllCards() => JALogger.Log("TODO: Unsuspend all cards");
    private void OnSuspendAllCards() => JALogger.Log("TODO: Suspend all cards");
    private void OnCreateVocabNote(string text) => JALogger.Log($"TODO: Create vocab note: {text}");
    private void OnCreateSentenceNote(string text) => JALogger.Log($"TODO: Create sentence note: {text}");
    private void OnCreateKanjiNote(string text) => JALogger.Log($"TODO: Create kanji note: {text}");
}
