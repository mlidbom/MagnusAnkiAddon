from typing import Callable

import aqt
from aqt.browser import Browser

from note.mynote import MyNote
from note.sentencenote import SentenceNote
from note.wanikanjinote import WaniKanjiNote
from note.waniradicalnote import WaniRadicalNote
from note.wanivocabnote import WaniVocabNote
from parsing import textparser
from parsing.janome_extensions.parsed_word import ParsedWord
from sysutils.ui_utils import UIUtils
from wanikani.wani_constants import Wani, Mine


class Builtin:
    Note = "note"
    Tag = "tag"
    Deck = "deck"
    Card = "card"

question = "Q"
reading = "Reading"
answer = "A"

card_listen = f"{Builtin.Card}:{Wani.WaniVocabNoteType.Card.Listening}"
card_read = f"{Builtin.Card}:{Wani.WaniVocabNoteType.Card.Reading}"

note_kanji = f"{Builtin.Note}:{Wani.NoteType.Kanji}"
note_vocab = f"{Builtin.Note}:{Wani.NoteType.Vocab}"

tag_uk = f"tag:{Mine.Tags.UsuallyKanaOnly}"

vocab_read = f"({note_vocab} {card_read})"

def question_wildcard(query:str) -> str: return f"{question}:*{query}"
def reading_wildcard(query:str) -> str: return f"{reading}:*{query}"
def answer_wildcard(query:str) -> str: return f"{answer}:*{query}"

def single_vocab_wildcard(query:str) -> str: return f"{vocab_read} ({question}:*{query}* OR {reading}:*{query}* OR {answer}:*{query}*)"
def single_vocab_exact(query) -> str:return f"{vocab_read} ({question}:{query} OR {reading}:re:\\b{query}\\b OR {answer}:re:\\b{query}\\b )"

def kanji_in_string(query) -> str: return f"{note_kanji} ( {' OR '.join([f'{question}:{char}' for char in query])} )"

def vocab_dependencies_lookup_query(vocab: WaniVocabNote) -> str:
    def single_vocab_clause(voc: ParsedWord) -> str:
        return f'({tag_uk} AND {reading}:{voc.word})' if voc.is_kana_only() else f'{question}:{voc.word}'

    def create_vocab_clause(text:str) -> str:
        dictionary_forms = [voc for voc in textparser.identify_words(text) if voc.word != vocab.get_question()]
        return f"({vocab_read} ({' OR '.join([single_vocab_clause(voc) for voc in dictionary_forms])})) OR " if dictionary_forms else ""

    def create_vocab_vocab_clause() -> str:
        return create_vocab_clause(vocab.get_question())

    def create_kanji_clause() -> str:
        return f"note:{Wani.NoteType.Kanji} ( {' OR '.join([f'{Wani.KanjiFields.question}:{char}' for char in vocab.get_question()])} )"

    return f'''{create_vocab_vocab_clause()} ({create_kanji_clause()})'''

def do_lookup_and_show_previewer(text: str) -> None:
    do_lookup(text)
    UIUtils.activate_preview()


def do_lookup(text) -> None:
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()


def lookup_promise(search: Callable[[], str]) -> Callable[[],None]: return lambda: do_lookup_and_show_previewer(search())

def sentence_vocab_lookup(sentence:SentenceNote) -> str: return text_vocab_lookup(sentence.get_active_question())

def vocab_with_kanji(note:WaniKanjiNote) -> str: return f"{vocab_read} Q:*{note.get_question()}*"

def text_vocab_lookup(text:str) -> str:
    def voc_clause(voc: ParsedWord) -> str:
        return f'({tag_uk} AND Reading:{voc.word})' if voc.is_kana_only() else f'Q:{voc.word}'

    dictionary_forms = textparser.identify_words(text)
    return f"{vocab_read} ({' OR '.join([voc_clause(voc) for voc in dictionary_forms])})"

def vocab_compounds_lookup(note:WaniVocabNote) -> str:
    def voc_clause(voc: ParsedWord) -> str:
        return f'({tag_uk} AND Reading:{voc.word})' if voc.is_kana_only() else f'Q:{voc.word}'

    vocab_word = note.get_question()
    dictionary_forms = [comp for comp in textparser.identify_words(vocab_word) if comp.word != vocab_word]

    return f"{vocab_read} ({' OR '.join([voc_clause(voc) for voc in dictionary_forms])})" if dictionary_forms else ""


def lookup_dependencies(note: MyNote):
    # noinspection PyTypeChecker
    type_map: dict[type, Callable[[], str]] = {
        WaniVocabNote: lambda: vocab_dependencies_lookup_query(note),
        WaniKanjiNote: lambda: vocab_with_kanji(note),
        SentenceNote: lambda: sentence_vocab_lookup(note),
        WaniRadicalNote: lambda: "",
        MyNote: lambda: ""
    }

    search = type_map[type(note)]()
    if search:
        do_lookup_and_show_previewer(search)
        UIUtils.activate_reviewer()