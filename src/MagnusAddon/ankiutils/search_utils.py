from typing import Callable, Iterable

import aqt
from aqt.browser import Browser

import parsing.tree_parsing.tree_parser # noqa
from parsing.tree_parsing.tree_parser_node import TreeParserNode
from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.kanjinote import KanjiNote
from note.radicalnote import RadicalNote
from note.vocabnote import VocabNote
from parsing import textparser
from parsing.janome_extensions.parsed_word import ParsedWord
from ankiutils.ui_utils import UIUtils
from note.note_constants import NoteFields, Mine, MyNoteFields, NoteTypes
from sysutils.typed import checked_cast


class Builtin:
    Note = "note"
    Tag = "tag"
    Deck = "deck"
    Card = "card"

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

def field_word(field:str, query:str) -> str: return f"""{field}:re:\\b{query}\\b"""

def question_wildcard(query:str) -> str: return f"{question}:*{query}"
def reading_wildcard(query:str) -> str: return f"{reading}:*{query}"
def answer_wildcard(query:str) -> str: return f"{answer}:*{query}"

def single_vocab_wildcard(query:str) -> str: return f"{vocab_read} ({forms}:*{query}* OR {reading}:*{query}* OR {answer}:*{query}*)"
def single_vocab_by_question_reading_or_answer_exact(query) -> str:return f"{vocab_read} ({field_word(forms, query)} OR {field_word(reading, query)} OR {field_word(answer, query)})"
def single_vocab_by_form_exact(query) -> str:return f"{vocab_read} {field_word(forms, query)}"


def kanji_in_string(query) -> str: return f"{note_kanji} ( {' OR '.join([f'{question}:{char}' for char in query])} )"

def vocab_dependencies_lookup_query(vocab: VocabNote) -> str:
    def single_vocab_clause(voc: ParsedWord) -> str:
        return f'{field_word(forms, voc.word)}'

    def create_vocab_clause(text:str) -> str:
        dictionary_forms = [voc for voc in textparser.identify_words(text)]
        return f"({vocab_read} ({' OR '.join([single_vocab_clause(voc) for voc in dictionary_forms])})) OR " if dictionary_forms else ""

    def create_vocab_vocab_clause() -> str:
        return create_vocab_clause(vocab.get_question())

    def create_kanji_clause() -> str:
        return f"{note_kanji} ( {' OR '.join([f'{question}:{char}' for char in vocab.get_question()])} )"

    return f'''{create_vocab_vocab_clause()} ({create_kanji_clause()})'''

def do_lookup_and_show_previewer(text: str) -> None:
    do_lookup(text)
    UIUtils.activate_preview()


def do_lookup(text) -> None:
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()


def lookup_promise(search: Callable[[], str]) -> Callable[[],None]: return lambda: do_lookup_and_show_previewer(search())

def sentence_exact(sentence: str) -> str:
    return f"""{note_sentence} {question}:"{sentence}" """

def sentence_vocab_lookup(sentence:SentenceNote) -> str: return text_vocab_lookup(sentence.get_active_question())

def vocab_with_kanji(note:KanjiNote) -> str: return f"{vocab_read} {forms}:*{note.get_question()}*"

def vocab_clause(voc: ParsedWord) -> str:
    return f"""{field_word(forms, voc.word)}"""

def node_vocab_clause(voc: TreeParserNode) -> str:
    search_base = voc.is_show_base_in_sentence_breakdown()
    search_surface = voc.is_show_surface_in_sentence_breakdown()

    base_query = f"""{field_word(forms, voc.base)}"""
    surface_query = f"""{field_word(forms, voc.surface)}"""

    if not search_base and not search_surface: raise Exception("Asked to search, but both base and surface excluded")

    if search_base and not search_surface:
        return base_query


    return f"""({base_query} OR {surface_query})""" if search_base else surface_query

def text_vocab_lookup(text:str) -> str:
    dictionary_forms = textparser.identify_words(text)
    return vocabs_lookup(dictionary_forms)

def vocab_lookup(vocab:ParsedWord) -> str: return vocabs_lookup([vocab])

def node_vocab_lookup(node:TreeParserNode) -> str: return node_vocabs_lookup([node])

def node_vocabs_lookup(dictionary_forms: list[TreeParserNode]) -> str:
    return f"{vocab_read} ({' OR '.join([node_vocab_clause(voc) for voc in dictionary_forms])})"

def vocabs_lookup(dictionary_forms: list[ParsedWord]) -> str:
    return f"{vocab_read} ({' OR '.join([vocab_clause(voc) for voc in dictionary_forms])})"


def vocab_compounds_lookup(note:VocabNote) -> str:
    vocab_word = note.get_question()
    dictionary_forms = [comp for comp in textparser.identify_words(vocab_word) if comp.word != vocab_word]

    return f"{vocab_read} ({' OR '.join([vocab_clause(voc) for voc in dictionary_forms])})" if dictionary_forms else ""


def lookup_dependencies(note: JPNote):
    # noinspection PyTypeChecker
    type_map: dict[type, Callable[[], str]] = {
        VocabNote: lambda: vocab_dependencies_lookup_query(checked_cast(VocabNote, note)),
        KanjiNote: lambda: vocab_with_kanji(checked_cast(KanjiNote, note)),
        SentenceNote: lambda: sentence_vocab_lookup(checked_cast(SentenceNote, note)),
        RadicalNote: lambda: "",
        JPNote: lambda: ""
    }

    search = type_map[type(note)]()
    if search:
        do_lookup(search)
        UIUtils.activate_reviewer()


def fetch_kanji_by_kanji(kanji: Iterable[str]) -> str:
    return f"""note:{NoteTypes.Kanji} ({" OR ".join([f"{NoteFields.Kanji.question}:{kan}" for kan in kanji])})"""


def lookup_text_object(text: str):
    return " OR ".join(f"{question}:{search.strip()}" for search in text.split(","))