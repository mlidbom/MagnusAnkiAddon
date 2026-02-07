using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.UI.Anki;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;

namespace JAStudio.UI.Menus;

/// <summary>
/// Sentence note-specific menu builders.
/// Corresponds to notes/sentence/main.py in Python.
/// </summary>
public static class SentenceNoteMenus
{
    public static SpecMenuItem BuildNoteActionsMenuSpec(SentenceNote sentence)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Note actions"),
            new List<SpecMenuItem>
            {
                BuildOpenMenuSpec(sentence),
                BuildRemoveMenuSpec(sentence),
                BuildRemoveUserMenuSpec(sentence)
            }
        );
    }

    private static SpecMenuItem BuildOpenMenuSpec(SentenceNote sentence)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Highlighted Vocab"), 
                () => AnkiFacade.ExecuteLookup(Core.TemporaryServiceCollection.Instance.QueryBuilder.VocabsLookupStrings(sentence.Configuration.HighlightedWords))),
            SpecMenuItem.Command(ShortcutFinger.Home2("Highlighted Vocab Read Card"), 
                () => AnkiFacade.ExecuteLookup(Core.TemporaryServiceCollection.Instance.QueryBuilder.VocabsLookupStringsReadCard(sentence.Configuration.HighlightedWords))),
            SpecMenuItem.Command(ShortcutFinger.Home3("Kanji"), 
                () => AnkiFacade.ExecuteLookup(Core.TemporaryServiceCollection.Instance.QueryBuilder.KanjiInString(string.Join("", sentence.ExtractKanji())))),
            SpecMenuItem.Command(ShortcutFinger.Home4("Parsed words"), 
                () => AnkiFacade.ExecuteLookup(Core.TemporaryServiceCollection.Instance.QueryBuilder.NotesByIds(GetParsedWordsNoteIds(sentence))))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home1("Open"), items);
    }

    private static SpecMenuItem BuildRemoveMenuSpec(SentenceNote sentence)
    {
        var hasHighlightedWords = sentence.Configuration.HighlightedWords.Any();
        var hasIncorrectMatches = sentence.Configuration.IncorrectMatches.Get().Any();
        var hasHiddenMatches = sentence.Configuration.HiddenMatches.Get().Any();
        var hasSourceComments = sentence.SourceComments.HasValue();

        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("All highlighted"), 
                () => sentence.Configuration.ResetHighlightedWords(), null, null, hasHighlightedWords),
            SpecMenuItem.Command(ShortcutFinger.Home2("All incorrect matches"), 
                () => sentence.Configuration.IncorrectMatches.Reset(), null, null, hasIncorrectMatches),
            SpecMenuItem.Command(ShortcutFinger.Home3("All hidden matches"), 
                () => sentence.Configuration.HiddenMatches.Reset(), null, null, hasHiddenMatches),
            SpecMenuItem.Command(ShortcutFinger.Home4("Source comments"), 
                () => sentence.SourceComments.Empty(), null, null, hasSourceComments)
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home2("Remove"), items);
    }

    private static SpecMenuItem BuildRemoveUserMenuSpec(SentenceNote sentence)
    {
        var hasUserComments = sentence.User.Comments.HasValue();
        var hasUserAnswer = sentence.User.Answer.HasValue();
        var hasUserQuestion = sentence.User.Question.HasValue();

        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("comments"), 
                () => sentence.User.Comments.Empty(), null, null, hasUserComments),
            SpecMenuItem.Command(ShortcutFinger.Home2("answer"), 
                () => sentence.User.Answer.Empty(), null, null, hasUserAnswer),
            SpecMenuItem.Command(ShortcutFinger.Home3("question"), 
                () => sentence.User.Question.Empty(), null, null, hasUserQuestion)
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home3("Remove User"), items);
    }

    public static SpecMenuItem BuildViewMenuSpec()
    {
        // View menu with config toggles
        var config = Core.TemporaryServiceCollection.Instance.App.Config();
        var items = new List<SpecMenuItem>();

        // Add toggles for sentence view configuration
        for (int i = 0; i < config.SentenceViewToggles.Count; i++)
        {
            var toggle = config.SentenceViewToggles[i];
            items.Add(SpecMenuItem.Command(
                ShortcutFinger.FingerByPriorityOrder(i, toggle.Title),
                () => toggle.SetValue(!toggle.GetValue())));
        }

        // Add the "Toggle all auto yield flags" action
        items.Add(SpecMenuItem.Command(
            ShortcutFinger.FingerByPriorityOrder(items.Count, "Toggle all sentence auto yield compound last token flags (Ctrl+Shift+Alt+d)"),
            () => config.ToggleAllSentenceDisplayAutoYieldFlags()));

        return SpecMenuItem.Submenu(ShortcutFinger.Home5("View"), items);
    }

    private static IEnumerable<long> GetParsedWordsNoteIds(SentenceNote sentence)
    {
        var parsingResult = sentence.ParsingResult.Get();
        var vocabIds = parsingResult.ParsedWords
            .Where(p => p.VocabId != -1)
            .Select(p => (long)p.VocabId)
            .Distinct();
        return vocabIds;
    }
}
