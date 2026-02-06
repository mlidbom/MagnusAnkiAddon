using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.UI.Utils;
using SpecMenuItem = JAStudio.UI.Menus.UIAgnosticMenuStructure.MenuItem;

namespace JAStudio.UI.Menus;

/// <summary>
/// Vocab string menu builders (selection/clipboard context menus).
/// Corresponds to notes/vocab/string_menu.py in Python.
/// </summary>
public static class VocabStringMenus
{
    public static SpecMenuItem BuildStringMenuSpec(string text, VocabNote vocab)
    {
        return SpecMenuItem.Submenu(
            ShortcutFinger.Home1("Current note actions"),
            new List<SpecMenuItem>
            {
                BuildAddMenuSpec(text, vocab),
                BuildSetMenuSpec(text, vocab),
                BuildRemoveMenuSpec(text, vocab),
                BuildSentenceMenuSpec(text, vocab)
                // TODO: Create combined menu (prefix/postfix operations)
            }
        );
    }

    private static SpecMenuItem BuildAddMenuSpec(string text, VocabNote vocab)
    {
        var synonyms = vocab.RelatedNotes.Synonyms.Strings();
        var antonyms = vocab.RelatedNotes.Antonyms.Strings();
        var seeAlso = vocab.RelatedNotes.SeeAlso.Strings();
        var confusedWith = vocab.RelatedNotes.ConfusedWith.Get();
        var perfectSynonyms = vocab.RelatedNotes.PerfectSynonyms.Get();
        var forms = vocab.Forms.AllSet();

        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Synonym"),
                () => vocab.RelatedNotes.Synonyms.Add(text), null, null, !synonyms.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Home2("Synonyms transitively one level"),
                () => vocab.RelatedNotes.Synonyms.AddTransitivelyOneLevel(text)),
            SpecMenuItem.Command(ShortcutFinger.Home3("Confused with"),
                () => vocab.RelatedNotes.ConfusedWith.Add(text), null, null, !confusedWith.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Home4("Antonym"),
                () => vocab.RelatedNotes.Antonyms.Add(text), null, null, !antonyms.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Home5("Form"),
                () => vocab.Forms.Add(text), null, null, !forms.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Up1("See also"),
                () => vocab.RelatedNotes.SeeAlso.Add(text), null, null, !seeAlso.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Down1("Perfect synonym, automatically synchronize answers"),
                () => vocab.RelatedNotes.PerfectSynonyms.AddOverwritingTheAnswerOfTheAddedSynonym(text), null, null, !perfectSynonyms.Contains(text))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home1("Add"), items);
    }

    private static SpecMenuItem BuildSetMenuSpec(string text, VocabNote vocab)
    {
        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Ergative twin"),
                () => vocab.RelatedNotes.ErgativeTwin.Set(text)),
            SpecMenuItem.Command(ShortcutFinger.Home2("Derived from"),
                () => vocab.RelatedNotes.DerivedFrom.Set(text))
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home2("Set"), items);
    }

    private static SpecMenuItem BuildRemoveMenuSpec(string text, VocabNote vocab)
    {
        var synonyms = vocab.RelatedNotes.Synonyms.Strings();
        var antonyms = vocab.RelatedNotes.Antonyms.Strings();
        var seeAlso = vocab.RelatedNotes.SeeAlso.Strings();
        var confusedWith = vocab.RelatedNotes.ConfusedWith.Get();
        var perfectSynonyms = vocab.RelatedNotes.PerfectSynonyms.Get();
        var forms = vocab.Forms.AllSet();
        var ergativeTwin = vocab.RelatedNotes.ErgativeTwin.Get();
        var derivedFrom = vocab.RelatedNotes.DerivedFrom.Get();

        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Synonym"),
                () => vocab.RelatedNotes.Synonyms.Remove(text), null, null, synonyms.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Home2("Confused with"),
                () => vocab.RelatedNotes.ConfusedWith.Remove(text), null, null, confusedWith.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Home3("Antonym"),
                () => vocab.RelatedNotes.Antonyms.Remove(text), null, null, antonyms.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Home4("Ergative twin"),
                () => vocab.RelatedNotes.ErgativeTwin.Remove(), null, null, text == ergativeTwin),
            SpecMenuItem.Command(ShortcutFinger.Home5("Form"),
                () => vocab.Forms.Remove(text), null, null, forms.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Up1("See also"),
                () => vocab.RelatedNotes.SeeAlso.Remove(text), null, null, seeAlso.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Down1("Perfect synonym"),
                () => vocab.RelatedNotes.PerfectSynonyms.Remove(text), null, null, perfectSynonyms.Contains(text)),
            SpecMenuItem.Command(ShortcutFinger.Down2("Derived from"),
                () => vocab.RelatedNotes.DerivedFrom.Set(""), null, null, text == derivedFrom)
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home3("Remove"), items);
    }

    private static SpecMenuItem BuildSentenceMenuSpec(string text, VocabNote vocab)
    {
        var sentences = Core.App.Col().Sentences.WithQuestion(text);
        var hasSentences = sentences.Count > 0;
        var disambiguationName = vocab.Question.DisambiguationName;

        bool isHighlighted = hasSentences && sentences[0].Configuration.HighlightedWords.Contains(disambiguationName);

        var items = new List<SpecMenuItem>
        {
            SpecMenuItem.Command(ShortcutFinger.Home1("Add Highlight"),
                () => {
                    if (sentences.Count > 0)
                        sentences[0].Configuration.AddHighlightedWord(disambiguationName);
                }, null, null, hasSentences && !isHighlighted),
            SpecMenuItem.Command(ShortcutFinger.Home2("Remove highlight"),
                () => {
                    foreach (var sent in sentences)
                        sent.Configuration.RemoveHighlightedWord(disambiguationName);
                }, null, null, hasSentences && isHighlighted),
            SpecMenuItem.Command(ShortcutFinger.Home3("Remove-sentence: Mark as incorrect match in sentence"),
                () => {
                    foreach (var sent in sentences)
                        sent.Configuration.IncorrectMatches.AddGlobal(disambiguationName);
                }, null, null, hasSentences)
        };

        return SpecMenuItem.Submenu(ShortcutFinger.Home4("Sentence"), items);
    }
}
