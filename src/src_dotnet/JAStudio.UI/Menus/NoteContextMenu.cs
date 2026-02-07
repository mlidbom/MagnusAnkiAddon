using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.UI.Anki;
using JAStudio.UI.Utils;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;

namespace JAStudio.UI.Menus;

/// <summary>
/// Main context menu coordinator - delegates to note-type-specific menu builders.
/// Corresponds to common.py in Python.
/// </summary>
public class NoteContextMenu
{
    readonly Core.TemporaryServiceCollection _services;
    readonly VocabNoteMenus _vocabNoteMenus;
    readonly KanjiNoteMenus _kanjiNoteMenus;
    readonly SentenceNoteMenus _sentenceNoteMenus;
    readonly OpenInAnkiMenus _openInAnkiMenus;
    readonly VocabStringMenus _vocabStringMenus;

    public NoteContextMenu(Core.TemporaryServiceCollection services)
    {
        _services = services;
        _vocabNoteMenus = new VocabNoteMenus(services);
        _kanjiNoteMenus = new KanjiNoteMenus(services);
        _sentenceNoteMenus = new SentenceNoteMenus(services);
        _openInAnkiMenus = new OpenInAnkiMenus(services);
        _vocabStringMenus = new VocabStringMenus(services);
    }

    /// <summary>
    /// Build context menu for a vocab note as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildVocabContextMenuSpec(int vocabId, string selection, string clipboard)
    {
        var vocab = _services.App.Col().Vocab.WithIdOrNone(vocabId);
        if (vocab == null)
            return [];

        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, "vocab", vocab));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, "vocab", vocab));

        menuItems.Add(_vocabNoteMenus.BuildNoteActionsMenuSpec(vocab));
        menuItems.Add(BuildUniversalNoteActionsMenuSpec(vocab));
        menuItems.Add(_vocabNoteMenus.BuildViewMenuSpec());

        return menuItems;
    }

    /// <summary>
    /// Build context menu for a kanji note as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildKanjiContextMenuSpec(int kanjiId, string selection, string clipboard)
    {
        var kanji = _services.App.Col().Kanji.WithIdOrNone(kanjiId);
        if (kanji == null)
            return [];

        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, "kanji", kanji));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, "kanji", kanji));

        menuItems.Add(_kanjiNoteMenus.BuildNoteActionsMenuSpec(kanji));
        menuItems.Add(BuildUniversalNoteActionsMenuSpec(kanji));
        menuItems.Add(_kanjiNoteMenus.BuildViewMenuSpec());

        return menuItems;
    }

    /// <summary>
    /// Build context menu for a sentence note as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildSentenceContextMenuSpec(int sentenceId, string selection, string clipboard)
    {
        var sentence = _services.App.Col().Sentences.WithIdOrNone(sentenceId);
        if (sentence == null)
            return [];

        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, "sentence", sentence));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, "sentence", sentence));

        menuItems.Add(_sentenceNoteMenus.BuildNoteActionsMenuSpec(sentence));
        menuItems.Add(BuildUniversalNoteActionsMenuSpec(sentence));
        menuItems.Add(_sentenceNoteMenus.BuildViewMenuSpec());

        return menuItems;
    }

    /// <summary>
    /// Build context menu when no note is available as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildGenericContextMenuSpec(string selection, string clipboard)
    {
        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, null, null));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, null, null));

        return menuItems;
    }

    /// <summary>
    /// Build context menu for a vocab note and convert to Avalonia MenuItems.
    /// </summary>
    public List<Avalonia.Controls.MenuItem> BuildVocabContextMenu(int vocabId, string selection, string clipboard)
    {
        var specs = BuildVocabContextMenuSpec(vocabId, selection, clipboard);
        return ConvertToAvaloniaMenuItems(specs);
    }

    /// <summary>
    /// Build context menu for a kanji note and convert to Avalonia MenuItems.
    /// </summary>
    public List<Avalonia.Controls.MenuItem> BuildKanjiContextMenu(int kanjiId, string selection, string clipboard)
    {
        var specs = BuildKanjiContextMenuSpec(kanjiId, selection, clipboard);
        return ConvertToAvaloniaMenuItems(specs);
    }

    /// <summary>
    /// Build context menu for a sentence note and convert to Avalonia MenuItems.
    /// </summary>
    public List<Avalonia.Controls.MenuItem> BuildSentenceContextMenu(int sentenceId, string selection, string clipboard)
    {
        var specs = BuildSentenceContextMenuSpec(sentenceId, selection, clipboard);
        return ConvertToAvaloniaMenuItems(specs);
    }

    /// <summary>
    /// Build generic context menu and convert to Avalonia MenuItems.
    /// </summary>
    public List<Avalonia.Controls.MenuItem> BuildGenericContextMenu(string selection, string clipboard)
    {
        var specs = BuildGenericContextMenuSpec(selection, clipboard);
        return ConvertToAvaloniaMenuItems(specs);
    }

    // String menu builders (for selection/clipboard)
    SpecMenuItem BuildSelectionMenuSpec(string selection, string? noteType, JPNote? note)
    {
        var truncated = TruncateText(selection, 40);
        var menuItems = BuildStringMenuSpec(selection, noteType, note);

        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1($"Selection: \"{truncated}\""),
            menuItems
        );
    }

    SpecMenuItem BuildClipboardMenuSpec(string clipboard, string? noteType, JPNote? note)
    {
        var truncated = TruncateText(clipboard, 40);
        var menuItems = BuildStringMenuSpec(clipboard, noteType, note);

        return SpecMenuItem.Submenu(
            ShortcutFinger.Home2($"Clipboard: \"{truncated}\""),
            menuItems
        );
    }

    List<SpecMenuItem> BuildStringMenuSpec(string text, string? noteType, JPNote? note)
    {
        return
        [
           BuildCurrentNoteActionsSubmenuSpec(text, noteType, note),
           _openInAnkiMenus.BuildOpenInAnkiMenuSpec(() => text),
           WebSearchMenus.BuildWebSearchMenuSpec(() => text),
           BuildMatchingNotesSubmenuSpec(text),
           BuildCreateNoteSubmenuSpec(text),
           SpecMenuItem.Command(ShortcutFinger.Down1($"Reparse matching sentences"), () => OnReparseMatchingSentences(text))
        ];
    }

    SpecMenuItem BuildCurrentNoteActionsSubmenuSpec(string text, string? noteType, JPNote? note)
    {
        // Delegate to note-type-specific string menu builders
        if (noteType == "vocab" && note is VocabNote vocab)
        {
            return _vocabStringMenus.BuildStringMenuSpec(text, vocab);
        }

        if (noteType == "kanji" && note is KanjiNote kanji)
        {
            return KanjiStringMenus.BuildStringMenuSpec(text, kanji);
        }

        if (noteType == "sentence" && note is SentenceNote sentence)
        {
            return SentenceStringMenus.BuildStringMenuSpec(sentence, text);
        }

        return SpecMenuItem.Submenu(ShortcutFinger.Home1("Current note actions"), new List<SpecMenuItem>());
    }

    SpecMenuItem BuildUniversalNoteActionsMenuSpec(JPNote note)
    {
        var hasSuspendedCards = note.HasSuspendedCards();
        var hasActiveCards = note.HasActiveCards();

        return SpecMenuItem.Submenu(
            ShortcutFinger.Home4("Universal note actions"),
            new List<SpecMenuItem>
            {
                SpecMenuItem.Command(ShortcutFinger.Home1("Open in previewer"),
                    () => OnOpenInPreviewer(note)),
                SpecMenuItem.Command(ShortcutFinger.Home3("Unsuspend all cards"),
                    () => note.UnsuspendAllCards(), null, null, hasSuspendedCards),
                SpecMenuItem.Command(ShortcutFinger.Home4("Suspend all cards"),
                    () => note.SuspendAllCards(), null, null, hasActiveCards)
            }
        );
    }

    SpecMenuItem BuildMatchingNotesSubmenuSpec(string text)
    {
        // Find notes that exactly match the search text
        var vocabs = _services.App.Col().Vocab.WithQuestionPreferDisambiguationName(text).ToList();
        var sentences = _services.App.Col().Sentences.WithQuestion(text);
        var kanjis = text.Length == 1
            ? _services.App.Col().Kanji.WithAnyKanjiIn([text])
            : [];

        // Only show submenu if any notes match
        if (!vocabs.Any() && !sentences.Any() && !kanjis.Any())
        {
            return SpecMenuItem.Submenu(ShortcutFinger.Home4("Exactly matching notes"), new List<SpecMenuItem>());
        }

        var items = new List<SpecMenuItem>
        {
            BuildUniversalNoteActionsMenuSpec(ShortcutFinger.Home1("Vocab Actions"), vocabs.FirstOrDefault()),
            BuildUniversalNoteActionsMenuSpec(ShortcutFinger.Home2("Sentence Actions"), sentences.FirstOrDefault()),
            BuildUniversalNoteActionsMenuSpec(ShortcutFinger.Home3("Kanji Actions"), kanjis.FirstOrDefault())
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home4("Exactly matching notes"), items);
    }

    SpecMenuItem BuildUniversalNoteActionsMenuSpec(string label, JPNote? note)
    {
        if (note == null)
        {
            return SpecMenuItem.Submenu(label, new List<SpecMenuItem>());
        }

        var hasSuspendedCards = note.HasSuspendedCards();
        var hasActiveCards = note.HasActiveCards();

        return SpecMenuItem.Submenu(
            label,
            new List<SpecMenuItem>
            {
                SpecMenuItem.Command(ShortcutFinger.Home1("Open in previewer"),
                    () => OnOpenInPreviewer(note)),
                SpecMenuItem.Command(ShortcutFinger.Home3("Unsuspend all cards"),
                    () => note.UnsuspendAllCards(), null, null, hasSuspendedCards),
                SpecMenuItem.Command(ShortcutFinger.Home4("Suspend all cards"),
                    () => note.SuspendAllCards(), null, null, hasActiveCards)
            }
        );
    }

    SpecMenuItem BuildCreateNoteSubmenuSpec(string text)
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

    // Utility methods
    static string TruncateText(string text, int maxLength)
    {
        if (text.Length <= maxLength)
            return text;
        return text.Substring(0, maxLength) + "...";
    }

    static List<Avalonia.Controls.MenuItem> ConvertToAvaloniaMenuItems(List<SpecMenuItem> specs)
    {
        var result = new List<Avalonia.Controls.MenuItem>();
        foreach (var spec in specs)
            result.Add(AvaloniaMenuAdapter.ToAvalonia(spec));
        return result;
    }

    // Action handlers
    void OnOpenInPreviewer(JPNote note)
    {
        var query = _services.QueryBuilder.NotesLookup([note]);
        AnkiFacade.ExecuteLookupAndShowPreviewer(query);
    }

    void OnReparseMatchingSentences(string text)
    {
        try
        {
            _services.LocalNoteUpdater.ReparseMatchingSentences(text);
            AnkiFacade.Refresh();
            AnkiFacade.ShowTooltip($"Reparsed sentences matching: {text}", 3000);
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to reparse matching sentences: {ex.Message}");
            AnkiFacade.ShowTooltip($"Failed to reparse: {ex.Message}", 5000);
        }
    }

    void OnCreateVocabNote(string text)
    {
        try
        {
            var newVocab = _services.VocabNoteFactory.CreateWithDictionary(text);
            _services.LocalNoteUpdater.ReparseSentencesForVocab(newVocab);

            var query = _services.QueryBuilder.NotesLookup([newVocab]);
            AnkiFacade.ExecuteLookupAndShowPreviewer(query);
            AnkiFacade.Refresh();
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to create vocab note: {ex.Message}");
            AnkiFacade.ShowTooltip($"Failed to create vocab note: {ex.Message}", 5000);
        }
    }

    void OnCreateSentenceNote(string text)
    {
        try
        {
            var noteServices = _services.NoteServices;
            var newSentence = SentenceNote.Create(noteServices, text);

            var query = _services.QueryBuilder.NotesLookup([newSentence]);
            AnkiFacade.ExecuteLookupAndShowPreviewer(query);
            AnkiFacade.Refresh();
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to create sentence note: {ex.Message}");
            AnkiFacade.ShowTooltip($"Failed to create sentence note: {ex.Message}", 5000);
        }
    }

    void OnCreateKanjiNote(string text)
    {
        try
        {
            var noteServices = _services.NoteServices;
            // Create with placeholder values - user will need to fill them in
            var newKanji = KanjiNote.Create(noteServices, text, "TODO", "", "");

            var query = _services.QueryBuilder.NotesLookup([newKanji]);
            AnkiFacade.ExecuteLookupAndShowPreviewer(query);
            AnkiFacade.Refresh();
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to create kanji note: {ex.Message}");
            AnkiFacade.ShowTooltip($"Failed to create kanji note: {ex.Message}", 5000);
        }
    }
}
