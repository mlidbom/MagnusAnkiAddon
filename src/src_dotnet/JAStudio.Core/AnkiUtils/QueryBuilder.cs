using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.AnkiUtils;

/// <summary>
/// Builds Anki search query strings for finding notes and cards.
/// Ported from jastudio/ankiutils/query_builder.py
/// </summary>
public class QueryBuilder
{
   readonly TemporaryServiceCollection _services;

   internal QueryBuilder(TemporaryServiceCollection services)
   {
      _services = services;
   }
   
    private const string ExcludedDeckSubstring = "*Excluded*";

    /// <summary>
    /// Combines clauses with OR, wrapping in parentheses if multiple clauses.
    /// </summary>
    private static string OrClauses(IEnumerable<string> clauses)
    {
        var clauseList = clauses.ToList();
        return clauseList.Count == 1 ? clauseList[0] : $"({string.Join(" OR ", clauseList)})";
    }

    /// <summary>
    /// Creates a field search for whole word matches using regex word boundaries.
    /// </summary>
    private static string FieldContainsWord(string field, params string[] words)
    {
        return OrClauses(words.Select(word => $"\"{field}:re:\\\\b{word}\\\\b\""));
    }

    /// <summary>
    /// Creates a field search for substring matches using wildcards.
    /// </summary>
    private static string FieldContainsString(string field, params string[] words)
    {
        return OrClauses(words.Select(word => $"\"{field}:*{word}*\""));
    }

    /// <summary>
    /// Search for sentence notes containing the given word.
    /// If exact=false, searches for all forms of vocab notes matching the word.
    /// Ported from sentence_search()
    /// </summary>
    public static string SentenceSearch(string word, bool exact = false)
    {
        var result = $"{Builtin.Note}:{NoteTypes.Sentence} ";

        string FormQuery(string form) =>
            $"(({MyNoteFields.Question}:*{form}* OR {FieldContainsWord(NoteFieldsConstants.Sentence.ParsingResult, form)}))";

        if (!exact)
        {
            var vocabs = App.Col().Vocab.WithForm(word).ToList();
            if (vocabs.Any())
            {
                var forms = vocabs.SelectMany(voc => voc.Forms.AllList()).Distinct().ToList();
                return result + "(" + string.Join("　OR ", forms.Select(FormQuery)) + ")";
            }
        }

        return result + $"({FormQuery(word)})";
    }

    /// <summary>
    /// Search for sentences that potentially match a vocab word.
    /// Ported from potentially_matching_sentences_for_vocab()
    /// </summary>
    public static string PotentiallyMatchingSentencesForVocab(VocabNote vocab)
    {
        var searchStrings = vocab.MatchingConfiguration.RequiresForbids.Surface.IsRequired
            ? vocab.Forms.AllList().ToList()
            : vocab.Conjugator.GetStemsForAllForms().Concat(vocab.Forms.AllList()).ToList();

        return $"{Builtin.Note}:{NoteTypes.Sentence} {FieldContainsString(MyNoteFields.Question, searchStrings.ToArray())}";
    }

    /// <summary>
    /// Creates a query to find notes by their JPNote instances.
    /// Ported from notes_lookup()
    /// </summary>
    public static string NotesLookup(IEnumerable<JPNote> notes)
    {
        return NotesByIds(notes.Select(n => (long)n.GetId()));
    }

    /// <summary>
    /// Creates a query to find notes by their IDs.
    /// Ported from notes_by_id()
    /// </summary>
    public static string NotesByIds(IEnumerable<long> noteIds)
    {
        var ids = noteIds.ToList();
        return ids.Count > 0 ? $"{NoteFieldsConstants.NoteId}:{string.Join(",", ids)}" : "";
    }

    /// <summary>
    /// Search for vocab notes using wildcard matching on forms, reading, or answer.
    /// Ported from single_vocab_wildcard()
    /// </summary>
    public static string SingleVocabWildcard(string form)
    {
        return $"{Builtin.Note}:{NoteTypes.Vocab} ({NoteFieldsConstants.Vocab.UserForms}:*{form}* OR {NoteFieldsConstants.Vocab.ReadingKana}:*{form}* OR {MyNoteFields.Answer}:*{form}*)";
    }

    /// <summary>
    /// Search for vocab notes by exact word match in forms, reading, or answer.
    /// Ported from single_vocab_by_question_reading_or_answer_exact()
    /// </summary>
    public static string SingleVocabByQuestionReadingOrAnswerExact(string search)
    {
        var hiraganaSearch = KanaUtils.KatakanaToHiragana(search);
        return $"{Builtin.Note}:{NoteTypes.Vocab} ({FieldContainsWord(NoteFieldsConstants.Vocab.UserForms, search)} OR {FieldContainsWord(NoteFieldsConstants.Vocab.ReadingKana, hiraganaSearch)} OR {FieldContainsWord(MyNoteFields.Answer, search)})";
    }

    /// <summary>
    /// Search for vocab notes by exact form match.
    /// Ported from single_vocab_by_form_exact()
    /// </summary>
    public static string SingleVocabByFormExact(string form)
    {
        return $"{Builtin.Note}:{NoteTypes.Vocab} {FieldContainsWord(NoteFieldsConstants.Vocab.UserForms, form)}";
    }

    /// <summary>
    /// Search for vocab reading cards by exact form match.
    /// Ported from single_vocab_by_form_exact_read_card_only()
    /// </summary>
    public static string SingleVocabByFormExactReadCardOnly(string form)
    {
        return $"({SingleVocabByFormExact(form)}) {Builtin.Card}:{NoteFieldsConstants.VocabNoteType.Card.Reading}";
    }

    /// <summary>
    /// Search for kanji notes for all kanji characters in the string.
    /// Ported from kanji_in_string()
    /// </summary>
    public static string KanjiInString(string text)
    {
        var kanjiClauses = text.Select(c => $"{MyNoteFields.Question}:{c}");
        return $"{Builtin.Note}:{NoteTypes.Kanji} ( {string.Join(" OR ", kanjiClauses)} )";
    }

    /// <summary>
    /// Search for vocab notes containing a specific kanji.
    /// Ported from vocab_with_kanji()
    /// </summary>
    public static string VocabWithKanji(KanjiNote kanji)
    {
        return $"{Builtin.Note}:{NoteTypes.Vocab} {NoteFieldsConstants.Vocab.UserForms}:*{kanji.GetQuestion()}*";
    }

    /// <summary>
    /// Search for vocab notes by dictionary forms extracted from text.
    /// Ported from text_vocab_lookup()
    /// </summary>
    public static string TextVocabLookup(string text)
    {
        var dictionaryForms = TextAnalysis.FromText(text).AllWordsStrings();
        return VocabsLookup(dictionaryForms);
    }

    /// <summary>
    /// Creates a vocab clause for a single form.
    /// Ported from vocab_clause()
    /// </summary>
    private static string VocabClause(string form)
    {
        return FieldContainsWord(NoteFieldsConstants.Vocab.UserForms, form);
    }

    /// <summary>
    /// Search for vocab notes matching any of the given dictionary forms.
    /// Ported from vocabs_lookup()
    /// </summary>
    public static string VocabsLookup(IEnumerable<string> dictionaryForms)
    {
        var forms = dictionaryForms.ToList();
        var clauses = forms.Select(VocabClause);
        return $"{Builtin.Note}:{NoteTypes.Vocab} ({string.Join(" OR ", clauses)})";
    }

    /// <summary>
    /// Search for vocab notes matching any of the given words (exact word match).
    /// Ported from vocabs_lookup_strings()
    /// </summary>
    public static string VocabsLookupStrings(IEnumerable<string> words)
    {
        var wordList = words.ToList();
        var clauses = wordList.Select(word => FieldContainsWord(NoteFieldsConstants.Vocab.UserForms, word));
        return $"{Builtin.Note}:{NoteTypes.Vocab} ({string.Join(" OR ", clauses)})";
    }

    /// <summary>
    /// Search for vocab reading cards matching any of the given words.
    /// Ported from vocabs_lookup_strings_read_card()
    /// </summary>
    public static string VocabsLookupStringsReadCard(IEnumerable<string> words)
    {
        return $"{VocabsLookupStrings(words)} {Builtin.Card}:{NoteFieldsConstants.VocabNoteType.Card.Reading}";
    }

    /// <summary>
    /// Search for kanji notes whose readings contain the given reading part.
    /// Ported from kanji_with_reading_part()
    /// </summary>
    public static string KanjiWithReadingPart(string readingPart)
    {
        var hiraganaReading = KanaUtils.AnythingToHiragana(readingPart);
        return $"{Builtin.Note}:{NoteTypes.Kanji} ({NoteFieldsConstants.Kanji.ReadingOn}:*{hiraganaReading}* OR {NoteFieldsConstants.Kanji.ReadingKun}:*{hiraganaReading}*)";
    }

    /// <summary>
    /// Search for notes with exact question match or form match.
    /// Ported from exact_matches()
    /// </summary>
    public static string ExactMatches(string question)
    {
        return $"{MyNoteFields.Question}:\"{question}\" OR {FieldContainsWord(NoteFieldsConstants.Vocab.UserForms, question)}";
    }

    /// <summary>
    /// Search for exact matches excluding sentence notes.
    /// Ported from exact_matches_no_sentences()
    /// </summary>
    public static string ExactMatchesNoSentences(string question)
    {
        return $"({ExactMatches(question)}) -{Builtin.Note}:{NoteTypes.Sentence}";
    }

    /// <summary>
    /// Search for exact matches on reading cards, excluding sentences and excluded decks.
    /// Ported from exact_matches_no_sentences_reading_cards()
    /// </summary>
    public static string ExactMatchesNoSentencesReadingCards(string question)
    {
        return $"({ExactMatchesNoSentences(question)}) {Builtin.Card}:{NoteFieldsConstants.VocabNoteType.Card.Reading} -{Builtin.Deck}:{ExcludedDeckSubstring}";
    }

    /// <summary>
    /// Search for Immersion Kit sentence notes.
    /// Ported from immersion_kit_sentences()
    /// </summary>
    public static string ImmersionKitSentences()
    {
        return $"\"{Builtin.Note}:{NoteTypes.ImmersionKit}\"";
    }

    /// <summary>
    /// Search for kanji notes containing all specified radicals.
    /// Ported from kanji_with_radicals_in_string()
    /// </summary>
    public static string KanjiWithRadicalsInString(string search)
    {
        var radicals = search.Trim().Replace(",", "").Replace(" ", "").ToCharArray().ToHashSet();
        
        bool KanjiContainsAllRadicals(KanjiNote kanji)
        {
            var kanjiRadicals = kanji.GetRadicals().ToHashSet();
            return radicals.All(r => kanjiRadicals.Contains(r.ToString()));
        }

        var matchingKanji = radicals
            .SelectMany(radical => App.Col().Kanji.WithRadical(radical.ToString()))
            .Distinct()
            .Where(KanjiContainsAllRadicals)
            .ToList();

        return NotesLookup(matchingKanji);
    }

    /// <summary>
    /// Search for a card by its ID.
    /// Ported from open_card_by_id()
    /// </summary>
    public static string OpenCardById(long cardId)
    {
        return $"cid:{cardId}";
    }

    /// <summary>
    /// Search for kanji notes whose meaning contains the search string.
    /// Ported from kanji_with_meaning()
    /// </summary>
    public static string KanjiWithMeaning(string search)
    {
        return $"{Builtin.Note}:{NoteTypes.Kanji} ({MyNoteFields.Answer}:*{search}*)";
    }

    /// <summary>
    /// Search for vocab dependencies (vocab and kanji that a word depends on).
    /// Ported from vocab_dependencies_lookup_query()
    /// </summary>
    public static string VocabDependenciesLookupQuery(VocabNote vocab)
    {
        string CreateVocabClause(string text)
        {
            var dictionaryForms = TextAnalysis.FromText(text).AllWordsStrings();
            if (!dictionaryForms.Any())
                return "";
                
            var clauses = dictionaryForms.Select(VocabClause);
            return $"({Builtin.Note}:{NoteTypes.Vocab} ({string.Join(" OR ", clauses)})) OR ";
        }
        
        string CreateKanjiClause()
        {
            var kanjiClauses = vocab.GetQuestion().Select(c => $"{MyNoteFields.Question}:{c}");
            return $"{Builtin.Note}:{NoteTypes.Kanji} ( {string.Join(" OR ", kanjiClauses)} )";
        }
        
        var vocabVocabClause = CreateVocabClause(vocab.GetQuestion());
        var kanjiClause = CreateKanjiClause();
        
        return $"{vocabVocabClause}({kanjiClause})";
    }
}
