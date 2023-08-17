from typing import Callable

import aqt
from PyQt6.QtWidgets import QMenu
from aqt.browser import Browser

from parsing import janomeutils, textparser
from parsing.janomeutils import ParsedWord
from sysutils.utils import UIUtils
from wanikani.wani_constants import Wani

_vocab_read_cards = f"(note:{Wani.NoteType.Vocab} card:*read*)"

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
    menu.addAction(name, anki_lookup(lambda: f"{_vocab_read_cards} Vocab:{vocab}"))

def add_text_vocab_lookup(menu: QMenu, name:str, text:str) -> None:
    def voc_clause(voc: ParsedWord) -> str:
        return f'(tag:_uk AND Reading:{voc.word})' if voc.is_kana_only() else f'Vocab:{voc.word}'

    def create_search_string() -> str:
        dictionary_forms = janomeutils.extract_dictionary_forms(text)
        return f"deck:*Vocab* deck:*Read* ({' OR '.join([voc_clause(voc) for voc in dictionary_forms])})"

    add_lookup_action_lambda(menu, name, create_search_string)

def add_text_vocab_lookup_v2(menu: QMenu, name:str, text:str) -> None:
    def voc_clause(voc: ParsedWord) -> str:
        return f'(tag:_uk AND Reading:{voc.word})' if voc.is_kana_only() else f'Vocab:{voc.word}'

    def create_search_string() -> str:
        dictionary_forms = textparser.identify_words2(text)
        return f"deck:*Vocab* deck:*Read* ({' OR '.join([voc_clause(voc) for voc in dictionary_forms])})"

    add_lookup_action_lambda(menu, name, create_search_string)

def anki_lookup(search: Callable[[], str]) -> Callable[[],None]:
    def do_lookup() -> None:
        browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
        browser.form.searchEdit.lineEdit().setText(search())
        browser.onSearchActivated()
        UIUtils.activate_preview()

    return do_lookup


def add_sentence_lookup(menu, name: str, search):
    add_lookup_action(menu, name, f"(deck:*sentence* deck:*listen*) (Expression:*{search}* OR Reading:*{search}* OR ParsedWords:*{search}*)")

