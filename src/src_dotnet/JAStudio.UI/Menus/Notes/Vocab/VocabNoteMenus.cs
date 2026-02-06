using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.AnkiUtils;
using JAStudio.Core.Note;
using JAStudio.UI.Anki;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;
using JAStudio.UI.Views;

namespace JAStudio.UI.Menus;

/// <summary>
/// Vocab note-specific menu builders.
/// Corresponds to notes/vocab/main.py in Python.
/// </summary>
public static class VocabNoteMenus
{
    public static SpecMenuItem BuildNoteActionsMenuSpec(VocabNote vocab)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home3("Note actions"),
            new List<SpecMenuItem>
            {
                BuildOpenMenuSpec(vocab),
                SpecMenuItem.Command(ShortcutFinger.Home2("Edit"), () => OnEditVocabFlags(vocab)),
                BuildCreateMenuSpec(vocab),
                BuildCopyMenuSpec(vocab),
                BuildMiscMenuSpec(vocab),
                BuildRemoveMenuSpec(vocab)
            }
        );
    }

    static SpecMenuItem BuildOpenMenuSpec(VocabNote vocab)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1("Open"),
            new List<SpecMenuItem?>
            {
                BuildOpenVocabMenuSpec(vocab),
                BuildOpenSentencesMenuSpec(vocab),
                BuildOpenKanjiMenuSpec(vocab),
                BuildOpenErgativeTwinMenuSpec(vocab)
            }.Where(m => m != null).ToList()!
        );
    }

    static SpecMenuItem BuildOpenVocabMenuSpec(VocabNote vocab)
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
            BuildOpenHomonymsMenuSpec(vocab),
            SpecMenuItem.Command(ShortcutFinger.Up2("Dependencies"),
                () => AnkiFacade.ExecuteLookup(QueryBuilder.VocabDependenciesLookupQuery(vocab)))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home1("Vocab"), items);
    }

    static SpecMenuItem BuildOpenHomonymsMenuSpec(VocabNote vocab)
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

    static SpecMenuItem BuildOpenSentencesMenuSpec(VocabNote vocab)
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

    static SpecMenuItem BuildOpenKanjiMenuSpec(VocabNote vocab)
    {
        var query = QueryBuilder.KanjiInString(vocab.GetQuestion());
        return SpecMenuItem.Command(ShortcutFinger.Home3("Kanji"),
            () => AnkiFacade.ExecuteLookup(query));
    }

    static SpecMenuItem? BuildOpenErgativeTwinMenuSpec(VocabNote vocab)
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

    static SpecMenuItem BuildCreateMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            BuildCreateCloneToFormMenuSpec(vocab),
            BuildCreateNounVariationsMenuSpec(vocab),
            BuildCreateVerbVariationsMenuSpec(vocab),
            BuildCreateMiscMenuSpec(vocab)
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home3("Create"), items);
    }

    static SpecMenuItem BuildCreateCloneToFormMenuSpec(VocabNote vocab)
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

    static SpecMenuItem BuildCreateNounVariationsMenuSpec(VocabNote vocab)
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

    static SpecMenuItem BuildCreateVerbVariationsMenuSpec(VocabNote vocab)
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

    static SpecMenuItem BuildCreateMiscMenuSpec(VocabNote vocab)
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

    static SpecMenuItem BuildCopyMenuSpec(VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Question"), () => CopyToClipboard(vocab.GetQuestion())),
            SpecMenuItem.Command(ShortcutFinger.Home2("Answer"), () => CopyToClipboard(vocab.GetAnswer())),
            SpecMenuItem.Command(ShortcutFinger.Home3("Definition (question:answer)"),
                () => CopyToClipboard($"{vocab.GetQuestion()}:{vocab.GetAnswer()}")),
            SpecMenuItem.Command(ShortcutFinger.Home4("Sentences: max 30"),
                () => CopyToClipboard(string.Join("\n", vocab.Sentences.All().Take(30)
                    .Select(s => s.Question.WithoutInvisibleSpace()))))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home4("Copy"), items);
    }

    static SpecMenuItem BuildMiscMenuSpec(VocabNote vocab)
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

    static SpecMenuItem BuildRemoveMenuSpec(VocabNote vocab)
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

    public static SpecMenuItem BuildViewMenuSpec() =>
       SpecMenuItem.Submenu(
          ShortcutFinger.Home5("View"),
          new List<SpecMenuItem>
          {
             // Empty in Python implementation
          }
       );

    // Action handlers
    static void OnEditVocabFlags(VocabNote vocab)
    {
        var dialog = new VocabFlagsDialog(vocab);
        dialog.Show();
    }

    static void OnAcceptVocabMeaning(VocabNote vocab)
    {
        var meaning = FormatVocabMeaning(vocab.GetAnswer());
        vocab.User.Answer.Set(meaning);
    }

    static string FormatVocabMeaning(string meaning) =>
       Core.SysUtils.ExStr.StripHtmlAndBracketMarkupAndNoiseCharacters(
          meaning.Replace(" SOURCE", "").Replace(", ", "/").Replace(" ", "-").ToLower());

    static void CopyToClipboard(string text)
    {
        try
        {
            Avalonia.Threading.Dispatcher.UIThread.Invoke(() =>
            {
                var topLevel = Avalonia.Application.Current?.ApplicationLifetime
                    is Avalonia.Controls.ApplicationLifetimes.IClassicDesktopStyleApplicationLifetime desktop
                    ? desktop.MainWindow
                    : null;

                if (topLevel?.Clipboard != null)
                {
                    topLevel.Clipboard.SetTextAsync(text).Wait();
                }
            });
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to copy to clipboard: {ex.Message}");
        }
    }
}
