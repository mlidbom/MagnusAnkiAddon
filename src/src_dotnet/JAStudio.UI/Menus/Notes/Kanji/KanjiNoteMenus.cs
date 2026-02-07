using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.UI.Anki;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;

namespace JAStudio.UI.Menus;

/// <summary>
/// Kanji note-specific menu builders.
/// Corresponds to notes/kanji/main.py in Python.
/// </summary>
public static class KanjiNoteMenus
{
    public static SpecMenuItem BuildNoteActionsMenuSpec(KanjiNote kanji)
    {
        var items = new List<SpecMenuItem>
        {
            BuildOpenMenuSpec(kanji),
            SpecMenuItem.Command(ShortcutFinger.Home5("Reset Primary Vocabs"), 
                () => kanji.SetPrimaryVocab(new List<string>()))
        };

        // Add conditional "Accept meaning" if no user answer exists
        if (string.IsNullOrEmpty(kanji.GetUserAnswer()))
        {
            items.Add(SpecMenuItem.Command(ShortcutFinger.Up1("Accept meaning"), 
                () => OnAcceptKanjiMeaning(kanji)));
        }

        items.Add(SpecMenuItem.Command(ShortcutFinger.Up2("Populate radicals from mnemonic tags"), 
            () => kanji.PopulateRadicalsFromMnemonicTags()));
        items.Add(SpecMenuItem.Command(ShortcutFinger.Up3("Bootstrap mnemonic from radicals"), 
            () => kanji.BootstrapMnemonicFromRadicals()));
        items.Add(SpecMenuItem.Command(ShortcutFinger.Up4("Reset mnemonic"), 
            () => kanji.SetUserMnemonic("")));

        return SpecMenuItem.Submenu(ShortcutFinger.Home3("Note actions"), items);
    }

    private static SpecMenuItem BuildOpenMenuSpec(KanjiNote kanji)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Primary Vocabs"), 
                () => AnkiFacade.ExecuteLookup(Core.TemporaryServiceCollection.Instance.QueryBuilder.VocabsLookupStrings(kanji.GetPrimaryVocab()))),
            SpecMenuItem.Command(ShortcutFinger.Home2("Vocabs"), 
                () => AnkiFacade.ExecuteLookup(Core.TemporaryServiceCollection.Instance.QueryBuilder.VocabWithKanji(kanji))),
            SpecMenuItem.Command(ShortcutFinger.Home3("Radicals"), 
                () => AnkiFacade.ExecuteLookup(Core.TemporaryServiceCollection.Instance.QueryBuilder.NotesLookup(kanji.GetRadicalsNotes()))),
            SpecMenuItem.Command(ShortcutFinger.Home4("Kanji"), 
                () => AnkiFacade.ExecuteLookup(Core.TemporaryServiceCollection.Instance.QueryBuilder.NotesLookup(
                    Core.TemporaryServiceCollection.Instance.App.Col().Kanji.WithRadical(kanji.GetQuestion())))),
            SpecMenuItem.Command(ShortcutFinger.Home5("Sentences"), 
                () => AnkiFacade.ExecuteLookup(Core.TemporaryServiceCollection.Instance.QueryBuilder.SentenceSearch(kanji.GetQuestion(), exact: true)))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home1("Open"), items);
    }

    public static SpecMenuItem BuildViewMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home5("View"),
            new List<SpecMenuItem>
            {
                // Empty in Python implementation
            }
        );
    }

    // Action handlers
    private static void OnAcceptKanjiMeaning(KanjiNote kanji)
    {
        var meaning = FormatKanjiMeaning(kanji.GetAnswer());
        kanji.SetUserAnswer(meaning);
    }

    private static string FormatKanjiMeaning(string meaning)
    {
        // Replace HTML and bracket markup with pipe separator
        var result = meaning
            .Replace("<", "|")
            .Replace(">", "|")
            .Replace("[", "|")
            .Replace("]", "|")
            .ToLower()
            .Replace("||", "|")
            .Replace("||", "|")
            .Replace("||", "|")
            .Replace(", ", "|")
            .Replace(" ", "-")
            .Replace("-|-", " | ");

        // Remove leading/trailing pipes
        result = result.TrimEnd('|').TrimStart('|');
        return result;
    }
}
