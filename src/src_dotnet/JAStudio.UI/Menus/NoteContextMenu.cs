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
    /// Build a context menu for a note with selection and clipboard.
    /// </summary>
    /// <param name="selection">Currently selected text (can be empty)</param>
    /// <param name="clipboard">Clipboard content (can be empty)</param>
    /// <param name="noteType">Type of note: "vocab", "kanji", "sentence", or null</param>
    public List<MenuItem> BuildContextMenu(string selection, string clipboard, string? noteType)
    {
        var menuItems = new List<MenuItem>();

        // Selection menu (if text is selected)
        if (!string.IsNullOrEmpty(selection))
        {
            menuItems.Add(BuildSelectionMenu(selection, noteType));
        }

        // Clipboard menu (if clipboard has content)
        if (!string.IsNullOrEmpty(clipboard))
        {
            menuItems.Add(BuildClipboardMenu(clipboard, noteType));
        }

        // Note actions menu
        menuItems.Add(BuildNoteActionsMenu(noteType));

        // Universal note actions menu
        menuItems.Add(BuildUniversalNoteActionsMenu());

        // View menu
        menuItems.Add(BuildViewMenu(noteType));

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

    private MenuItem BuildNoteActionsMenu(string? noteType)
    {
        var menuItems = new List<MenuItem>();

        // TODO: Add note-specific actions based on note type
        switch (noteType)
        {
            case "vocab":
                // TODO: Port from menus.notes.vocab.main.setup_note_menu
                menuItems.Add(CreateMenuItem("Vocab Actions (TODO)", () => { }));
                break;
            case "kanji":
                // TODO: Port from menus.notes.kanji.main.build_note_menu
                menuItems.Add(CreateMenuItem("Kanji Actions (TODO)", () => { }));
                break;
            case "sentence":
                // TODO: Port from menus.notes.sentence.main.build_note_menu
                menuItems.Add(CreateMenuItem("Sentence Actions (TODO)", () => { }));
                break;
        }

        return new MenuItem
        {
            Header = "Note actions",
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

    private MenuItem BuildViewMenu(string? noteType)
    {
        var menuItems = new List<MenuItem>();

        // TODO: Add view actions based on note type
        switch (noteType)
        {
            case "vocab":
            case "kanji":
            case "sentence":
                menuItems.Add(CreateMenuItem("View Actions (TODO)", () => { }));
                break;
        }

        return new MenuItem
        {
            Header = "View",
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
