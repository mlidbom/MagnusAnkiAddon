from __future__ import annotations

from typing import Iterable

from anki.notes import NoteId

from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.note_constants import Builtin, Mine, MyNoteFields, NoteFields, NoteTypes
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from language_services.janome_ex.word_extraction import word_extractor
from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
from sysutils import ex_str

question = MyNoteFields.question
reading = NoteFields.Vocab.Reading
answer = MyNoteFields.answer
forms = NoteFields.Vocab.Forms

card_listen = f"{Builtin.Card}:{NoteFields.VocabNoteType.Card.Listening}"
card_read = f"{Builtin.Card}:{NoteFields.VocabNoteType.Card.Reading}"

note_kanji = f"{Builtin.Note}:{NoteTypes.Kanji}"
note_vocab = f"{Builtin.Note}:{NoteTypes.Vocab}"
note_sentence = f"{Builtin.Note}:{NoteTypes.Sentence}"

tag_uk = f"tag:{Mine.Tags.UsuallyKanaOnly}"

vocab_read = f"({note_vocab} {card_read})"

def _or_clauses(clauses:list[str]) -> str:
    return clauses[0] if len(clauses) == 1 else f"""({" OR ".join(clauses)})"""


def field_contains_word(field:str, *words:str) -> str:
    return _or_clauses([f'''"{field}:re:\\b{query}\\b"''' for query in words])

def field_value_exact(field:str, *queries:str) -> str:
    return _or_clauses([f'''"{field}:{query}"''' for query in queries])

def single_vocab_wildcard(query:str) -> str: return f"{vocab_read} ({forms}:*{query}* OR {reading}:*{query}* OR {answer}:*{query}*)"
def single_vocab_by_question_reading_or_answer_exact(query: str) -> str:return f"{vocab_read} ({field_contains_word(forms, query)} OR {field_contains_word(reading, query)} OR {field_contains_word(answer, query)})"
def single_vocab_by_form_exact(query: str) -> str:return f"{vocab_read} {field_contains_word(forms, query)}"


def kanji_in_string(query: str) -> str: return f"{note_kanji} ( {' OR '.join([f'{question}:{char}' for char in query])} )"

def vocab_dependencies_lookup_query(vocab: VocabNote) -> str:
    def single_vocab_clause(voc: ExtractedWord) -> str:
        return f'{field_contains_word(forms, voc.word)}'

    def create_vocab_clause(text:str) -> str:
        dictionary_forms = [voc for voc in word_extractor.extract_words(text)]
        return f"({vocab_read} ({' OR '.join([single_vocab_clause(voc) for voc in dictionary_forms])})) OR " if dictionary_forms else ""

    def create_vocab_vocab_clause() -> str:
        return create_vocab_clause(vocab.get_question())

    def create_kanji_clause() -> str:
        return f"{note_kanji} ( {' OR '.join([f'{question}:{char}' for char in vocab.get_question()])} )"

    return f'''{create_vocab_vocab_clause()} ({create_kanji_clause()})'''


def sentence_exact(sentence: str) -> str:
    return f"""{note_sentence} {question}:"{sentence}" """

def sentence_vocab_lookup(sentence:SentenceNote) -> str: return text_vocab_lookup(sentence.get_question())

def vocab_with_kanji(note:KanjiNote) -> str: return f"{vocab_read} {forms}:*{note.get_question()}*"

def vocab_clause(voc: ExtractedWord) -> str:
    return f"""{field_contains_word(forms, voc.word)}"""

def text_vocab_lookup(text:str) -> str:
    dictionary_forms = word_extractor.extract_words(text)
    return vocabs_lookup(dictionary_forms)

def vocab_lookup(vocab:ExtractedWord) -> str: return vocabs_lookup([vocab])

def vocabs_lookup(dictionary_forms: list[ExtractedWord]) -> str:
    return f"{vocab_read} ({' OR '.join([vocab_clause(voc) for voc in dictionary_forms])})"


def vocab_compounds_lookup(note:VocabNote) -> str:
    vocab_word = note.get_question()
    dictionary_forms = [comp for comp in word_extractor.extract_words(vocab_word) if comp.word != vocab_word]

    return f"{vocab_read} ({' OR '.join([vocab_clause(voc) for voc in dictionary_forms])})" if dictionary_forms else ""



def fetch_kanji_by_kanji(kanji: Iterable[str]) -> str:
    return f"""note:{NoteTypes.Kanji} ({" OR ".join([f"{NoteFields.Kanji.question}:{kan}" for kan in kanji])})"""

def lookup_text_object(text: str) -> str:
    words = ex_str.extract_comma_separated_values(text)
    if text.isascii(): #probably radical answer
        return field_value_exact(answer, *words)
    else:
        return _or_clauses([field_value_exact(question, *words), field_contains_word(forms, *words)])

def notes_by_id(note_ids:list[NoteId]) -> str:
    return f"""nid:{",".join([str(note_id) for note_id in note_ids])}"""

def notes_by_note(notes:list[JPNote]) -> str:
    return notes_by_id([n.get_id() for n in notes])