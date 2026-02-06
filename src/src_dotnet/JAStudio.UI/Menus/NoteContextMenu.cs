using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.AnkiUtils;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.UI.Anki;
using JAStudio.UI.Utils;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using SpecMenuItem = JAStudio.UI.Menus.UIAgnosticMenuStructure.MenuItem;

namespace JAStudio.UI.Menus;

/// <summary>
/// Main context menu coordinator - delegates to note-type-specific menu builders.
/// Corresponds to common.py in Python.
/// </summary>
public class NoteContextMenu
{
    /// <summary>
    /// Build context menu for a vocab note as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildVocabContextMenuSpec(int vocabId, string selection, string clipboard)
    {
        var vocab = Core.App.Col().Vocab.WithIdOrNone(vocabId);
        if (vocab == null)
            return new List<SpecMenuItem>();

        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, "vocab", vocab));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, "vocab", vocab));

        menuItems.Add(VocabNoteMenus.BuildNoteActionsMenuSpec(vocab));
        menuItems.Add(BuildUniversalNoteActionsMenuSpec(vocab));
        menuItems.Add(VocabNoteMenus.BuildViewMenuSpec());

        return menuItems;
    }

    /// <summary>
    /// Build context menu for a kanji note as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildKanjiContextMenuSpec(int kanjiId, string selection, string clipboard)
    {
        var kanji = Core.App.Col().Kanji.WithIdOrNone(kanjiId);
        if (kanji == null)
            return new List<SpecMenuItem>();

        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, "kanji", kanji));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, "kanji", kanji));

        menuItems.Add(KanjiNoteMenus.BuildNoteActionsMenuSpec(kanji));
        menuItems.Add(BuildUniversalNoteActionsMenuSpec(kanji));
        menuItems.Add(KanjiNoteMenus.BuildViewMenuSpec());

        return menuItems;
    }

    /// <summary>
    /// Build context menu for a sentence note as UI-agnostic specifications.
    /// </summary>
    public List<SpecMenuItem> BuildSentenceContextMenuSpec(int sentenceId, string selection, string clipboard)
    {
        var sentence = Core.App.Col().Sentences.WithIdOrNone(sentenceId);
        if (sentence == null)
            return new List<SpecMenuItem>();

        var menuItems = new List<SpecMenuItem>();

        if (!string.IsNullOrEmpty(selection))
            menuItems.Add(BuildSelectionMenuSpec(selection, "sentence", sentence));

        if (!string.IsNullOrEmpty(clipboard))
            menuItems.Add(BuildClipboardMenuSpec(clipboard, "sentence", sentence));

        menuItems.Add(SentenceNoteMenus.BuildNoteActionsMenuSpec(sentence));
        menuItems.Add(BuildUniversalNoteActionsMenuSpec(sentence));
        menuItems.Add(SentenceNoteMenus.BuildViewMenuSpec());

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
    private SpecMenuItem BuildSelectionMenuSpec(string selection, string? noteType, JPNote? note)
    {
        var truncated = TruncateText(selection, 40);
        var menuItems = BuildStringMenuSpec(selection, noteType, note);

        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1($"Selection: \"{truncated}\""),
            menuItems
        );
    }

    private SpecMenuItem BuildClipboardMenuSpec(string clipboard, string? noteType, JPNote? note)
    {
        var truncated = TruncateText(clipboard, 40);
        var menuItems = BuildStringMenuSpec(clipboard, noteType, note);

        return SpecMenuItem.Submenu(
            ShortcutFinger.Home2($"Clipboard: \"{truncated}\""),
            menuItems
        );
    }

    private List<SpecMenuItem> BuildStringMenuSpec(string text, string? noteType, JPNote? note)
    {
        return new List<SpecMenuItem>
        {
            BuildCurrentNoteActionsSubmenuSpec(text, noteType, note),
            OpenInAnkiMenus.BuildOpenInAnkiMenuSpec(() => text),
            WebSearchMenus.BuildWebSearchMenuSpec(() => text),
            BuildMatchingNotesSubmenuSpec(text),
            BuildCreateNoteSubmenuSpec(text),
            SpecMenuItem.Command(ShortcutFinger.Down1($"Reparse matching sentences"), () => OnReparseMatchingSentences(text))
        };
    }

    private SpecMenuItem BuildCurrentNoteActionsSubmenuSpec(string text, string? noteType, JPNote? note)
    {
        // Delegate to note-type-specific string menu builders
        if (noteType == "vocab" && note is VocabNote vocab)
        {
            return VocabStringMenus.BuildStringMenuSpec(text, vocab);
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

    private SpecMenuItem BuildUniversalNoteActionsMenuSpec(JPNote note)
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

    private SpecMenuItem BuildMatchingNotesSubmenuSpec(string text)
    {
        // Find notes that exactly match the search text
        var vocabs = Core.App.Col().Vocab.WithQuestionPreferDisambiguationName(text).ToList();
        var sentences = Core.App.Col().Sentences.WithQuestion(text);
        var kanjis = text.Length == 1 
            ? Core.App.Col().Kanji.WithAnyKanjiIn(new List<string> { text })
            : new List<KanjiNote>();

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

    private SpecMenuItem BuildUniversalNoteActionsMenuSpec(string label, JPNote? note)
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

    // Utility methods
    private static string TruncateText(string text, int maxLength)
    {
        if (text.Length <= maxLength)
            return text;
        return text.Substring(0, maxLength) + "...";
    }

    private static List<Avalonia.Controls.MenuItem> ConvertToAvaloniaMenuItems(List<SpecMenuItem> specs)
    {
        var result = new List<Avalonia.Controls.MenuItem>();
        foreach (var spec in specs)
            result.Add(AvaloniaMenuAdapter.ToAvalonia(spec));
        return result;
    }

    // Action handlers
    private void OnOpenInPreviewer(JPNote note)
    {
        var query = QueryBuilder.NotesLookup(new[] { note });
        AnkiFacade.ExecuteLookupAndShowPreviewer(query);
    }
    
    private void OnReparseMatchingSentences(string text)
    {
        try
        {
            Core.Batches.LocalNoteUpdater.ReparseMatchingSentences(text);
            AnkiFacade.Refresh();
            AnkiFacade.ShowTooltip($"Reparsed sentences matching: {text}", 3000);
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to reparse matching sentences: {ex.Message}");
            AnkiFacade.ShowTooltip($"Failed to reparse: {ex.Message}", 5000);
        }
    }
    
    private void OnCreateVocabNote(string text)
    {
        try
        {
            var newVocab = VocabNoteFactory.CreateWithDictionary(text);
            Core.Batches.LocalNoteUpdater.ReparseSentencesForVocab(newVocab);
            
            var query = QueryBuilder.NotesLookup(new JPNote[] { newVocab });
            AnkiFacade.ExecuteLookupAndShowPreviewer(query);
            AnkiFacade.Refresh();
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to create vocab note: {ex.Message}");
            AnkiFacade.ShowTooltip($"Failed to create vocab note: {ex.Message}", 5000);
        }
    }
    
    private void OnCreateSentenceNote(string text)
    {
        try
        {
            var newSentence = SentenceNote.Create(text);
            
            var query = QueryBuilder.NotesLookup(new JPNote[] { newSentence });
            AnkiFacade.ExecuteLookupAndShowPreviewer(query);
            AnkiFacade.Refresh();
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to create sentence note: {ex.Message}");
            AnkiFacade.ShowTooltip($"Failed to create sentence note: {ex.Message}", 5000);
        }
    }
    
    private void OnCreateKanjiNote(string text)
    {
        try
        {
            // Create with placeholder values - user will need to fill them in
            var newKanji = KanjiNote.Create(text, "TODO", "", "");
            
            var query = QueryBuilder.NotesLookup(new JPNote[] { newKanji });
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
