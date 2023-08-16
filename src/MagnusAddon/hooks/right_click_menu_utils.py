from typing import Callable

import aqt
from PyQt6.QtWidgets import QMenu
from aqt.browser import Browser

from sysutils import janomeutils
from sysutils.janomeutils import ParsedWord
from sysutils.utils import UIUtils
from wanikani.wani_constants import Wani

_vocab_read_cards = f"(note:{Wani.NoteType.Vocab} card:*read*)"

def add_ui_action(menu: QMenu, name: str, callback: Callable[[], None]) -> None:
    menu.addAction(name, lambda: run_ui_action())

    def run_ui_action() -> None:
        callback()
        UIUtils.refresh()

def add_lookup_action(menu: QMenu, name: str, search: str) -> None:
    menu.addAction(name, lambda: anki_lookup(search))

def add_single_vocab_lookup_action(menu: QMenu, name:str, vocab:str) -> None:
    menu.addAction(name, lambda: anki_lookup(f"{_vocab_read_cards} Vocab:{vocab}"))

def add_text_vocab_lookup(menu: QMenu, name:str, text:str) -> None:
    def voc_clause(voc: ParsedWord) -> str:
        return f'(tag:_uk AND Reading:{voc.word})' if voc.is_kana_only() else f'Vocab:{voc.word}'

    dictionary_forms = janomeutils.extract_dictionary_forms(text)
    add_lookup_action(menu,
                      name,
                      f"deck:*Vocab* deck:*Read* ({' OR '.join([voc_clause(voc) for voc in dictionary_forms])})")

def anki_lookup(search: str) -> None:
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(search)
    browser.onSearchActivated()
    UIUtils.activate_preview()


def add_sentence_lookup(menu, name: str, search):
    add_lookup_action(menu, name, f"(deck:*sentence* deck:*listen*) (Expression:*{search}* OR Reading:*{search}* OR ParsedWords:*{search}*)")

