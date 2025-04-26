from __future__ import annotations

from typing import Sequence

from anki.notes import NoteId

from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.note_constants import Builtin, MyNoteFields, NoteFields, NoteTypes, SentenceNoteFields
from note.radicalnote import RadicalNote
from note.vocabnote import VocabNote
from language_services.janome_ex.word_extraction import word_extractor
from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord

f_question = MyNoteFields.question
f_reading = NoteFields.Vocab.Reading
f_answer = MyNoteFields.answer
f_forms = NoteFields.Vocab.Forms

card_read = f"{Builtin.Card}:{NoteFields.VocabNoteType.Card.Reading}"

note_kanji = f"{Builtin.Note}:{NoteTypes.Kanji}"
note_vocab = f"{Builtin.Note}:{NoteTypes.Vocab}"
note_sentence = f"{Builtin.Note}:{NoteTypes.Sentence}"
excluded_deck_substring = "*Excluded*"
deck_excluded = f'''{Builtin.Deck}:{excluded_deck_substring}'''

note_vocab = note_vocab

def _or_clauses(clauses:list[str]) -> str:
    return clauses[0] if len(clauses) == 1 else f"""({" OR ".join(clauses)})"""


def field_contains_word(field:str, *words:str) -> str:
    return _or_clauses([f'''"{field}:re:\\b{query}\\b"''' for query in words])

def field_contains_string(field:str, *words:str) -> str:
    return _or_clauses([f'''"{field}:*{query}*"''' for query in words])

def sentence_search(word:str, exact:bool = False) -> str:
    result = f"""{note_sentence} """

    def form_query(form:str) -> str:
        return f"""(-{field_contains_word(SentenceNoteFields.user_excluded_vocab, form)} AND ({f_question}:*{form}* OR {field_contains_word(SentenceNoteFields.ParsedWords, form)} OR {field_contains_word(SentenceNoteFields.user_extra_vocab, form)}))"""

    if not exact:
        from ankiutils import app
        vocabs = app.col().vocab.with_form(word)
        if vocabs:
            forms = set().union(*[v.get_forms() for v in vocabs])
            return result + "(" + "　OR ".join([form_query(form) for form in forms]) + ")"

    return result + f"""({form_query(word)})"""

def sentence_with_any_vocab_form_in_question(word:VocabNote) -> str:
    search_strings = word.get_stems_for_all_forms() + list(word.get_forms())
    return f"""{note_sentence} {field_contains_string(f_question,  *search_strings)}"""


def notes_lookup(notes: Sequence[JPNote]) -> str:
    return f"""{NoteFields.note_id}:{",".join(str(note.get_id()) for note in notes)}""" if notes else ""

def single_vocab_wildcard(query:str) -> str: return f"{note_vocab} ({f_forms}:*{query}* OR {f_reading}:*{query}* OR {f_answer}:*{query}*)"
def single_vocab_by_question_exact(query: str) -> str:return f"{note_vocab} {f_question}={query}"
def single_vocab_by_question_reading_or_answer_exact(query: str) -> str:return f"{note_vocab} ({field_contains_word(f_forms, query)} OR {field_contains_word(f_reading, query)} OR {field_contains_word(f_answer, query)})"
def single_vocab_by_form_exact(query: str) -> str:return f"{note_vocab} {field_contains_word(f_forms, query)}"

def single_vocab_by_form_exact_read_card_only(query: str) -> str:return f"({single_vocab_by_form_exact(query)}) {card_read}"


def kanji_in_string(query: str) -> str: return f"{note_kanji} ( {' OR '.join([f'{f_question}:{char}' for char in query])} )"

def vocab_dependencies_lookup_query(vocab: VocabNote) -> str:
    def single_vocab_clause(voc: ExtractedWord) -> str:
        return f'{field_contains_word(f_forms, voc.word)}'

    def create_vocab_clause(text:str) -> str:
        dictionary_forms = [voc for voc in word_extractor.extract_words(text)]
        return f"({note_vocab} ({' OR '.join([single_vocab_clause(voc) for voc in dictionary_forms])})) OR " if dictionary_forms else ""

    def create_vocab_vocab_clause() -> str:
        return create_vocab_clause(vocab.get_question())

    def create_kanji_clause() -> str:
        return f"{note_kanji} ( {' OR '.join([f'{f_question}:{char}' for char in vocab.get_question()])} )"

    return f'''{create_vocab_vocab_clause()} ({create_kanji_clause()})'''

def vocab_with_kanji(note:KanjiNote) -> str: return f"{note_vocab} {f_forms}:*{note.get_question()}*"

def vocab_clause(voc: ExtractedWord) -> str:
    return f"""{field_contains_word(f_forms, voc.word)}"""

def text_vocab_lookup(text:str) -> str:
    dictionary_forms = word_extractor.extract_words(text)
    return vocabs_lookup(dictionary_forms)

def vocabs_lookup(dictionary_forms: list[ExtractedWord]) -> str:
    return f"{note_vocab} ({' OR '.join([vocab_clause(voc) for voc in dictionary_forms])})"

def vocabs_lookup_strings(words: list[str]) -> str:
    return f'''{note_vocab} ({' OR '.join([f"""{field_contains_word(f_forms, voc)}""" for voc in words])})'''

def vocabs_lookup_strings_read_card(words: list[str]) -> str:
    return f'''{vocabs_lookup_strings(words)} {card_read}'''

def notes_by_id(note_ids:list[NoteId]) -> str:
    return f"""nid:{",".join([str(note_id) for note_id in note_ids])}"""

def notes_by_note(notes:Sequence[JPNote]) -> str:
    return notes_by_id([n.get_id() for n in notes])

def kanji_with_radical(radical: RadicalNote) -> str:
    if radical.get_question():
        return f"note:{NoteTypes.Kanji} {NoteFields.Kanji.Radicals}:*{radical.get_question()}*"
    else:
        return f"note:{NoteTypes.Kanji} ({field_contains_word(NoteFields.Kanji.Radicals_Names, radical.get_answer())} OR {field_contains_word(NoteFields.Kanji.Radicals_Icons_Names, radical.get_answer())} )"

def kanji_with_kanji_radical(radical: KanjiNote) -> str:
    return f"note:{NoteTypes.Kanji} {NoteFields.Kanji.Radicals}:*{radical.get_question()}*"

def exact_matches(question: str) -> str:
    return f'''{f_question}:"{question}" OR {field_contains_word(f_forms, question)}'''

def exact_matches_no_sentences(question: str) -> str:
    return f'''({exact_matches(question)}) -{note_sentence}'''

def exact_matches_no_sentences_reading_cards(question: str) -> str:
    return f'''({exact_matches_no_sentences(question)}) {card_read} -{deck_excluded}'''

def immersion_kit_sentences() -> str:
    return f'''"{Builtin.Note}:{NoteTypes.immersion_kit}"'''
