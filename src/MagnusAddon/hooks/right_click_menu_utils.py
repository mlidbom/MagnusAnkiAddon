from typing import Callable

import aqt
from PyQt6.QtWidgets import QMenu
from aqt.browser import Browser

from ankiutils import search_utils as su
from note.wanivocabnote import WaniVocabNote
from parsing import textparser
from parsing.janome_extensions.parsed_word import ParsedWord
from sysutils.ui_utils import UIUtils
from wanikani.wani_constants import Wani

def add_ui_action(menu: QMenu, name: str, callback: Callable[[], None]) -> None:
    menu.addAction(name, lambda: run_ui_action())

    def run_ui_action() -> None:
        callback()
        UIUtils.refresh()

def add_lookup_action_lambda(menu: QMenu, name: str, search: Callable[[],str]) -> None:
    menu.addAction(name, anki_lookup(search))

def add_lookup_action(menu: QMenu, name: str, search: str) -> None:
    menu.addAction(name, anki_lookup(lambda: search))

def add_single_vocab_lookup_action(menu: QMenu, name:str, vocab:str) -> None:
    menu.addAction(name, anki_lookup(lambda: f"{su.vocab_read} Vocab:{vocab}"))

def add_text_vocab_lookup(menu: QMenu, name:str, text:str) -> None:
    def voc_clause(voc: ParsedWord) -> str:
        return f'(tag:_uk AND Reading:{voc.word})' if voc.is_kana_only() else f'Q:{voc.word}'

    def create_search_string() -> str:
        dictionary_forms = textparser.identify_words(text)
        return f"{su.vocab_read} ({' OR '.join([voc_clause(voc) for voc in dictionary_forms])})"

    add_lookup_action_lambda(menu, name, create_search_string)

def add_vocab_dependencies_lookup(menu: QMenu, name: str, vocab: WaniVocabNote):
    def single_vocab_clause(voc: ParsedWord) -> str:
        return f'(tag:_uk AND Reading:{voc.word})' if voc.is_kana_only() else f'Q:{voc.word}'

    def create_vocab_clause(text:str) -> str:
        dictionary_forms = textparser.identify_words(text)
        return f"{su.vocab_read} ({' OR '.join([single_vocab_clause(voc) for voc in dictionary_forms])})"

    def create_vocab_vocab_clause() -> str:
        return create_vocab_clause(vocab.get_question())

    def create_kanji_clause() -> str:
        return f"note:{Wani.NoteType.Kanji} ( {' OR '.join([f'{Wani.KanjiFields.question}:{char}' for char in vocab.get_question()])} )"

    def create_dependencies_lookup_query() -> str:
        return f'''({create_vocab_vocab_clause()}) OR ({create_kanji_clause()})'''

    add_lookup_action_lambda(menu, name, create_dependencies_lookup_query)


def anki_lookup(search: Callable[[], str]) -> Callable[[],None]:
    def do_lookup() -> None:
        browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
        browser.form.searchEdit.lineEdit().setText(search())
        browser.onSearchActivated()
        UIUtils.activate_preview()

    return do_lookup


def add_sentence_lookup(menu, name: str, search):
    add_lookup_action(menu, name, f"(deck:*sentence* deck:*listen*) (Q:*{search}* OR Reading:*{search}* OR ParsedWords:re:\b{search}\b)")

