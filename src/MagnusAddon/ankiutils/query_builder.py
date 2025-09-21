from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from note.note_constants import Builtin, MyNoteFields, NoteFields, NoteTypes, SentenceNoteFields
from queryablecollections.collections.q_set import QSet
from sysutils import kana_utils

if TYPE_CHECKING:
    from collections.abc import Iterable

    from anki.cards import CardId
    from anki.notes import NoteId
    from note.jpnote import JPNote
    from note.kanjinote import KanjiNote
    from note.vocabulary.vocabnote import VocabNote

f_question = MyNoteFields.question
f_reading = NoteFields.Vocab.Reading
f_answer = MyNoteFields.answer
f_forms = NoteFields.Vocab.Forms
f_reading_on = NoteFields.Kanji.Reading_On
f_reading_kun = NoteFields.Kanji.Reading_Kun

card_read = f"{Builtin.Card}:{NoteFields.VocabNoteType.Card.Reading}"

note_kanji = f"{Builtin.Note}:{NoteTypes.Kanji}"
note_vocab = f"{Builtin.Note}:{NoteTypes.Vocab}"
note_sentence = f"{Builtin.Note}:{NoteTypes.Sentence}"
excluded_deck_substring = "*Excluded*"
deck_excluded = f"""{Builtin.Deck}:{excluded_deck_substring}"""

note_vocab = note_vocab

def _or_clauses(clauses: list[str]) -> str:
    return clauses[0] if len(clauses) == 1 else f"""({" OR ".join(clauses)})"""

def field_contains_word(field: str, *words: str) -> str:
    return _or_clauses([f'''"{field}:re:\\b{query}\\b"''' for query in words])

def field_contains_string(field: str, *words: str) -> str:
    return _or_clauses([f'''"{field}:*{query}*"''' for query in words])

def sentence_search(word: str, exact: bool = False) -> str:
    result = f"""{note_sentence} """

    def form_query(form: str) -> str:
        return f"""(-{field_contains_word(SentenceNoteFields.user_excluded_vocab, form)} AND ({f_question}:*{form}* OR {field_contains_word(SentenceNoteFields.parsing_result, form)} OR {field_contains_word(SentenceNoteFields.user_extra_vocab, form)}))"""

    if not exact:
        vocabs = app.col().vocab.with_form(word)
        if vocabs:
            forms: set[str] = vocabs.select_many(lambda voc: voc.forms.all_list()).to_set()  # set(ex_sequence.flatten([v.forms.all_list() for v in vocabs]))
            return result + "(" + "　OR ".join([form_query(form) for form in forms]) + ")"

    return result + f"""({form_query(word)})"""

def potentially_matching_sentences_for_vocab(word: VocabNote) -> str:
    if word.matching_configuration.requires_forbids.exact_match.is_required:
        search_strings = word.forms.all_list()
    else:
        search_strings = word.conjugator.get_stems_for_all_forms() + word.forms.all_list()
        # we'd much rather catch too much than not enough here. False positives only slow things down a bit,
        # false negatives on the other hand, can totally confuse things, giving the user entirely the wrong idea about the value of a word when no/few matches are found.
        search_strings += [form[:-1] for form in word.forms.all_list() if (len(form) > 2 or kana_utils.contains_kanji(form)) and kana_utils.character_is_kana(form[-1])]
    return f"""{note_sentence} {field_contains_string(f_question, *search_strings)}"""

def sentences_with_question_substring(substring: str) -> str:
    return f"""{note_sentence} {field_contains_string(SentenceNoteFields.active_question, substring)}"""

def notes_lookup(notes: Iterable[JPNote]) -> str:
    return notes_by_id([note.get_id() for note in notes])

def notes_by_id(note_ids: list[NoteId]) -> str:
    return f"""{NoteFields.note_id}:{",".join([str(note_id) for note_id in note_ids])}""" if note_ids else ""

def single_vocab_wildcard(query: str) -> str: return f"{note_vocab} ({f_forms}:*{query}* OR {f_reading}:*{query}* OR {f_answer}:*{query}*)"

def single_vocab_by_question_reading_or_answer_exact(query: str) -> str:
    return f"{note_vocab} ({field_contains_word(f_forms, query)} OR {field_contains_word(f_reading, kana_utils.katakana_to_hiragana(query))} OR {field_contains_word(f_answer, query)})"

def single_vocab_by_form_exact(query: str) -> str: return f"{note_vocab} {field_contains_word(f_forms, query)}"

def single_vocab_by_form_exact_read_card_only(query: str) -> str: return f"({single_vocab_by_form_exact(query)}) {card_read}"

def kanji_in_string(query: str) -> str: return f"{note_kanji} ( {' OR '.join([f'{f_question}:{char}' for char in query])} )"

def vocab_dependencies_lookup_query(vocab: VocabNote) -> str:
    def single_vocab_clause(voc: str) -> str:
        return f"{field_contains_word(f_forms, voc)}"

    def create_vocab_clause(text: str) -> str:
        dictionary_forms = TextAnalysis.from_text(text).all_words_strings()
        return f"({note_vocab} ({' OR '.join([single_vocab_clause(voc) for voc in dictionary_forms])})) OR " if dictionary_forms else ""

    def create_vocab_vocab_clause() -> str:
        return create_vocab_clause(vocab.get_question())

    def create_kanji_clause() -> str:
        return f"{note_kanji} ( {' OR '.join([f'{f_question}:{char}' for char in vocab.get_question()])} )"

    return f"""{create_vocab_vocab_clause()} ({create_kanji_clause()})"""

def vocab_with_kanji(note: KanjiNote) -> str: return f"{note_vocab} {f_forms}:*{note.get_question()}*"

def vocab_clause(voc: str) -> str:
    return f"""{field_contains_word(f_forms, voc)}"""

def text_vocab_lookup(text: str) -> str:
    dictionary_forms = TextAnalysis.from_text(text).all_words_strings()
    return vocabs_lookup(dictionary_forms)

def vocabs_lookup(dictionary_forms: list[str]) -> str:
    return f"{note_vocab} ({' OR '.join([vocab_clause(voc) for voc in dictionary_forms])})"

def vocabs_lookup_strings(words: list[str]) -> str:
    return f'''{note_vocab} ({' OR '.join([f"""{field_contains_word(f_forms, voc)}""" for voc in words])})'''

def vocabs_lookup_strings_read_card(words: list[str]) -> str:
    return f"""{vocabs_lookup_strings(words)} {card_read}"""

def kanji_with_reading_part(reading_part: str) -> str:
    hiragana_reading_part = kana_utils.anything_to_hiragana(reading_part)
    return f"""note:{NoteTypes.Kanji} ({f_reading_on}:*{hiragana_reading_part}* OR {f_reading_kun}:*{hiragana_reading_part}*)"""

def exact_matches(question: str) -> str:
    return f"""{f_question}:"{question}" OR {field_contains_word(f_forms, question)}"""

def exact_matches_no_sentences(question: str) -> str:
    return f"""({exact_matches(question)}) -{note_sentence}"""

def exact_matches_no_sentences_reading_cards(question: str) -> str:
    return f"""({exact_matches_no_sentences(question)}) {card_read} -{deck_excluded}"""

def immersion_kit_sentences() -> str:
    return f'''"{Builtin.Note}:{NoteTypes.immersion_kit}"'''

def kanji_with_radicals_in_string(search: str) -> str:
    radicals = QSet(search.strip().replace(",", "").replace(" ", ""))
    def kanji_contails_all_radicals(kanji: KanjiNote) -> bool: return not any(rad for rad in radicals if rad not in kanji.get_radicals())
    return (radicals
            .select_many(lambda radical: app.col().kanji.with_radical(radical))
            .where(kanji_contails_all_radicals)
            .pipe(notes_lookup))

def open_card_by_id(card_id: CardId) -> str:
    return f"cid:{card_id}"

def kanji_with_meaning(search: str) -> str:
    return f"""{note_kanji} ({f_answer}:*{search}*)"""
