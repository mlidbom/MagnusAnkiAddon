using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core;
using JAStudio.Core.AnkiUtils;
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

        menuItems.Add(BuildKanjiNoteActionsMenuSpec(kanji));
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

        menuItems.Add(BuildSentenceNoteActionsMenuSpec(sentence));
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
                BuildVocabOpenMenuSpec(vocab),
                SpecMenuItem.Command(ShortcutFinger.Home2("Edit"), () => OnEditVocabFlags(vocab)),
                BuildVocabCreateMenuSpec(vocab),
                BuildVocabCopyMenuSpec(vocab),
                BuildVocabMiscMenuSpec(vocab),
                BuildVocabRemoveMenuSpec(vocab)
            }
        );
    }

    private SpecMenuItem BuildVocabOpenMenuSpec(VocabNote vocab)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1("Open"),
            new List<SpecMenuItem>
            {
                BuildVocabOpenVocabMenuSpec(vocab),
                BuildVocabOpenSentencesMenuSpec(vocab),
                BuildVocabOpenKanjiMenuSpec(vocab),
                BuildVocabOpenErgativeTwinMenuSpec(vocab)
            }.Where(m => m != null).ToList()!
        );
    }

    private SpecMenuItem BuildVocabOpenVocabMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Forms"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(vocab.Forms.AllListNotes()))),
            SpecMenuItem.Command(ShortcutFinger.Home2("Compound parts"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.VocabsLookupStrings(vocab.CompoundParts.All()))),
            SpecMenuItem.Command(ShortcutFinger.Home3("In compounds"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(vocab.RelatedNotes.InCompounds()))),
            SpecMenuItem.Command(ShortcutFinger.Home4("Synonyms"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(vocab.RelatedNotes.Synonyms.Notes()))),
            SpecMenuItem.Command(ShortcutFinger.Home5("See also"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(vocab.RelatedNotes.SeeAlso.Notes()))),
            BuildVocabOpenHomonymsMenuSpec(vocab),
            SpecMenuItem.Command(ShortcutFinger.Up2("Dependencies"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.VocabDependenciesLookupQuery(vocab)))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home1("Vocab"), items);
    }

    private SpecMenuItem BuildVocabOpenHomonymsMenuSpec(VocabNote vocab)
    {
        var readings = vocab.GetReadings();
        var items = new List<SpecMenuItem>();

        for (int i = 0; i < readings.Count; i++)
        {
            var reading = readings[i];
            items.Add(SpecMenuItem.Command(
                ShortcutFinger.FingerByPriorityOrder(i, $"Homonyms: {reading}"),
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(Core.App.Col().Vocab.WithReading(reading)))));
        }

        return SpecMenuItem.Submenu(ShortcutFinger.Up1("Homonyms"), items);
    }

    private SpecMenuItem BuildVocabOpenSentencesMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Sentences I'm Studying"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(vocab.Sentences.Studying()))),
            SpecMenuItem.Command(ShortcutFinger.Home2("Sentences"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(vocab.Sentences.All()))),
            SpecMenuItem.Command(ShortcutFinger.Home3("Sentences with primary form"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(vocab.Sentences.WithPrimaryForm()))),
            SpecMenuItem.Command(ShortcutFinger.Home4("Sentences with this word highlighted"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(vocab.Sentences.UserHighlighted()))),
            SpecMenuItem.Command(ShortcutFinger.Home5("Potentially matching sentences"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.PotentiallyMatchingSentencesForVocab(vocab))),
            SpecMenuItem.Command(ShortcutFinger.Up1("Marked invalid in sentences"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(vocab.Sentences.InvalidIn())))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home2("Sentences"), items);
    }

    private SpecMenuItem BuildVocabOpenKanjiMenuSpec(VocabNote vocab)
    {
        var query = QueryBuilder.KanjiInString(vocab.GetQuestion());
        return SpecMenuItem.Command(ShortcutFinger.Home3("Kanji"), 
            () => AnkiFacade.ExecuteLookup(query));
    }

    private SpecMenuItem? BuildVocabOpenErgativeTwinMenuSpec(VocabNote vocab)
    {
        var ergativeTwinQuestion = vocab.RelatedNotes.ErgativeTwin.Get();
        if (string.IsNullOrEmpty(ergativeTwinQuestion))
            return null;

        var ergativeTwinNotes = Core.App.Col().Vocab.WithQuestion(ergativeTwinQuestion);
        if (!ergativeTwinNotes.Any())
            return null;

        return SpecMenuItem.Command(ShortcutFinger.Home4("Ergative twin"), 
            () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(ergativeTwinNotes)));
    }

    private SpecMenuItem BuildVocabCreateMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            BuildVocabCreateCloneToFormMenuSpec(vocab),
            BuildVocabCreateNounVariationsMenuSpec(vocab),
            BuildVocabCreateVerbVariationsMenuSpec(vocab),
            BuildVocabCreateMiscMenuSpec(vocab)
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home3("Create"), items);
    }

    private SpecMenuItem BuildVocabCreateCloneToFormMenuSpec(VocabNote vocab)
    {
        var col = Core.App.Col();
        var formsWithNoVocab = vocab.Forms.AllSet()
            .Where(form => !col.Vocab.WithQuestion(form).Any())
            .ToList();

        var items = new List<SpecMenuItem>();
        for (int i = 0; i < formsWithNoVocab.Count; i++)
        {
            var form = formsWithNoVocab[i];
            items.Add(SpecMenuItem.Command(
                ShortcutFinger.FingerByPriorityOrder(i, form),
                () => vocab.Cloner.CloneToForm(form)));
        }

        return SpecMenuItem.Submenu(ShortcutFinger.Home1("Clone to form"), items);
    }

    private SpecMenuItem BuildVocabCreateNounVariationsMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("する-verb"), () => vocab.Cloner.CreateSuruVerb()),
            SpecMenuItem.Command(ShortcutFinger.Home2("します-verb"), () => vocab.Cloner.CreateShimasuVerb()),
            SpecMenuItem.Command(ShortcutFinger.Home3("な-adjective"), () => vocab.Cloner.CreateNaAdjective()),
            SpecMenuItem.Command(ShortcutFinger.Home4("の-adjective"), () => vocab.Cloner.CreateNoAdjective()),
            SpecMenuItem.Command(ShortcutFinger.Up1("に-adverb"), () => vocab.Cloner.CreateNiAdverb()),
            SpecMenuItem.Command(ShortcutFinger.Up2("と-adverb"), () => vocab.Cloner.CreateToAdverb())
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home2("Noun variations"), items);
    }

    private SpecMenuItem BuildVocabCreateVerbVariationsMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("ます-form"), () => vocab.Cloner.CreateMasuForm()),
            SpecMenuItem.Command(ShortcutFinger.Home2("て-form"), () => vocab.Cloner.CreateTeForm()),
            SpecMenuItem.Command(ShortcutFinger.Home3("た-form"), () => vocab.Cloner.CreateTaForm()),
            SpecMenuItem.Command(ShortcutFinger.Home4("ない-form"), () => vocab.Cloner.CreateNaiForm()),
            SpecMenuItem.Command(ShortcutFinger.Home5($"え-stem/godan-imperative {vocab.Cloner.SuffixToEStemPreview("")}"), 
                () => vocab.Cloner.SuffixToEStem("")),
            SpecMenuItem.Command(ShortcutFinger.Up1("ば-form"), () => vocab.Cloner.CreateBaForm()),
            SpecMenuItem.Command(ShortcutFinger.Up2("{receptive/passive}-form"), () => vocab.Cloner.CreateReceptiveForm()),
            SpecMenuItem.Command(ShortcutFinger.Up3("causative"), () => vocab.Cloner.CreateCausativeForm()),
            SpecMenuItem.Command(ShortcutFinger.Up4("imperative"), () => vocab.Cloner.CreateImperative()),
            SpecMenuItem.Command(ShortcutFinger.Down1("Potential-godan"), () => vocab.Cloner.CreatePotentialGodan())
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home3("Verb variations"), items);
    }

    private SpecMenuItem BuildVocabCreateMiscMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("く-form-of-い-adjective"), () => vocab.Cloner.CreateKuForm()),
            SpecMenuItem.Command(ShortcutFinger.Home2("さ-form-of-い-adjective"), () => vocab.Cloner.CreateSaForm()),
            SpecMenuItem.Command(ShortcutFinger.Home3("て-prefixed"), () => vocab.Cloner.CreateTePrefixedWord()),
            SpecMenuItem.Command(ShortcutFinger.Home4("お-prefixed"), () => vocab.Cloner.CreateOPrefixedWord()),
            SpecMenuItem.Command(ShortcutFinger.Home5("ん-suffixed"), () => vocab.Cloner.CreateNSuffixedWord()),
            SpecMenuItem.Command(ShortcutFinger.Up1("か-suffixed"), () => vocab.Cloner.CreateKaSuffixedWord())
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home4("Misc"), items);
    }

    private SpecMenuItem BuildVocabCopyMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Question"), () => CopyToClipboard(vocab.GetQuestion())),
            SpecMenuItem.Command(ShortcutFinger.Home2("Answer"), () => CopyToClipboard(vocab.GetAnswer())),
            SpecMenuItem.Command(ShortcutFinger.Home3("Definition (question:answer)"), 
                () => CopyToClipboard($"{vocab.GetQuestion()}: {vocab.GetAnswer()}")),
            SpecMenuItem.Command(ShortcutFinger.Home4("Sentences: max 30"), 
                () => CopyToClipboard(string.Join("\n", vocab.Sentences.All().Take(30)
                    .Select(s => s.Question.WithoutInvisibleSpace()))))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home4("Copy"), items);
    }

    private SpecMenuItem BuildVocabMiscMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Accept meaning"), 
                () => OnAcceptVocabMeaning(vocab), 
                null, null, !vocab.User.Answer.HasValue()),
            SpecMenuItem.Command(ShortcutFinger.Home2("Generate answer"), 
                () => vocab.GenerateAndSetAnswer()),
            SpecMenuItem.Command(ShortcutFinger.Home3("Reparse potentially matching sentences: (Only reparse all sentences is sure to catch everything)"), 
                () => Core.Batches.LocalNoteUpdater.ReparseSentencesForVocab(vocab)),
            SpecMenuItem.Command(ShortcutFinger.Home4("Repopulate TOS"), 
                () => vocab.PartsOfSpeech.SetAutomaticallyFromDictionary()),
            SpecMenuItem.Command(ShortcutFinger.Home5("Autogenerate compounds"), 
                () => vocab.CompoundParts.AutoGenerate())
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home5("Misc"), items);
    }

    private SpecMenuItem BuildVocabRemoveMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("User explanation"), 
                () => vocab.User.Explanation.Empty(), null, null, vocab.User.Explanation.HasValue()),
            SpecMenuItem.Command(ShortcutFinger.Home2("User explanation long"), 
                () => vocab.User.ExplanationLong.Empty(), null, null, vocab.User.ExplanationLong.HasValue()),
            SpecMenuItem.Command(ShortcutFinger.Home3("User mnemonic"), 
                () => vocab.User.Mnemonic.Empty(), null, null, vocab.User.Mnemonic.HasValue()),
            SpecMenuItem.Command(ShortcutFinger.Home4("User answer"), 
                () => vocab.User.Answer.Empty(), null, null, vocab.User.Answer.HasValue())
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Up1("Remove"), items);
    }

    private SpecMenuItem BuildVocabViewMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home5("View"),
            new List<SpecMenuItem>
            {
                // Empty in Python implementation
            }
        );
    }

    // Kanji-specific menus
    private SpecMenuItem BuildKanjiNoteActionsMenuSpec(KanjiNote kanji)
    {
        var items = new List<SpecMenuItem>
        {
            BuildKanjiOpenMenuSpec(kanji),
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

    private SpecMenuItem BuildKanjiOpenMenuSpec(KanjiNote kanji)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Primary Vocabs"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.VocabsLookupStrings(kanji.GetPrimaryVocab()))),
            SpecMenuItem.Command(ShortcutFinger.Home2("Vocabs"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.VocabWithKanji(kanji))),
            SpecMenuItem.Command(ShortcutFinger.Home3("Radicals"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(kanji.GetRadicalsNotes()))),
            SpecMenuItem.Command(ShortcutFinger.Home4("Kanji"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesLookup(
                    Core.App.Col().Kanji.WithRadical(kanji.GetQuestion())))),
            SpecMenuItem.Command(ShortcutFinger.Home5("Sentences"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.SentenceSearch(kanji.GetQuestion(), exact: true)))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home1("Open"), items);
    }

    private SpecMenuItem BuildKanjiViewMenuSpec()
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home5("View"),
            new List<SpecMenuItem>
            {
                // Empty in Python implementation
            }
        );
    }

    // Sentence-specific menus
    private SpecMenuItem BuildSentenceNoteActionsMenuSpec(SentenceNote sentence)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Note actions"),
            new List<SpecMenuItem>
            {
                BuildSentenceOpenMenuSpec(sentence),
                BuildSentenceRemoveMenuSpec(sentence),
                BuildSentenceRemoveUserMenuSpec(sentence)
            }
        );
    }

    private SpecMenuItem BuildSentenceOpenMenuSpec(SentenceNote sentence)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Highlighted Vocab"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.VocabsLookupStrings(sentence.Configuration.HighlightedWords))),
            SpecMenuItem.Command(ShortcutFinger.Home2("Highlighted Vocab Read Card"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.VocabsLookupStringsReadCard(sentence.Configuration.HighlightedWords))),
            SpecMenuItem.Command(ShortcutFinger.Home3("Kanji"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.KanjiInString(string.Join("", sentence.ExtractKanji())))),
            SpecMenuItem.Command(ShortcutFinger.Home4("Parsed words"), 
                () => AnkiFacade.ExecuteLookup(QueryBuilder.NotesByIds(GetParsedWordsNoteIds(sentence))))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home1("Open"), items);
    }

    private SpecMenuItem BuildSentenceRemoveMenuSpec(SentenceNote sentence)
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

    private SpecMenuItem BuildSentenceRemoveUserMenuSpec(SentenceNote sentence)
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

    private SpecMenuItem BuildSentenceViewMenuSpec()
    {
        // View menu with config toggles
        var config = Core.App.Config();
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

    private void OnAcceptVocabMeaning(VocabNote vocab)
    {
        var meaning = FormatVocabMeaning(vocab.GetAnswer());
        vocab.User.Answer.Set(meaning);
    }

    private void OnAcceptKanjiMeaning(KanjiNote kanji)
    {
        var meaning = FormatKanjiMeaning(kanji.GetAnswer());
        kanji.SetUserAnswer(meaning);
    }

    private static string FormatVocabMeaning(string meaning)
    {
        return Core.SysUtils.ExStr.StripHtmlAndBracketMarkupAndNoiseCharacters(
            meaning.Replace(" SOURCE", "").Replace(", ", "/").Replace(" ", "-").ToLower());
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

    private static void CopyToClipboard(string text)
    {
        try
        {
            // Note: Clipboard copying to be handled by Python layer for now
            // Avalonia clipboard requires a TopLevel (window) reference
            JALogger.Log($"Copy to clipboard requested: {text.Substring(0, Math.Min(50, text.Length))}...");
            
            // TODO: When we have full Avalonia window context, use:
            // var topLevel = Avalonia.Controls.TopLevel.GetTopLevel(someControl);
            // topLevel?.Clipboard?.SetTextAsync(text).GetAwaiter().GetResult();
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to copy to clipboard: {ex.Message}");
        }
    }
    
    private void OnReparseMatchingSentences(string text) => JALogger.Log($"TODO: Reparse matching sentences: {text}");
    private void OnOpenInPreviewer() => JALogger.Log("TODO: Open in previewer");
    private void OnUnsuspendAllCards() => JALogger.Log("TODO: Unsuspend all cards");
    private void OnSuspendAllCards() => JALogger.Log("TODO: Suspend all cards");
    private void OnCreateVocabNote(string text) => JALogger.Log($"TODO: Create vocab note: {text}");
    private void OnCreateSentenceNote(string text) => JALogger.Log($"TODO: Create sentence note: {text}");
    private void OnCreateKanjiNote(string text) => JALogger.Log($"TODO: Create kanji note: {text}");
}
