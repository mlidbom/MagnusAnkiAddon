from typing import Callable

from PyQt6.QtWidgets import QMenu

from ankiutils import query_builder as su
from ankiutils.app import ui_utils
from ankiutils.search_executor import lookup_promise
from note.vocabnote import VocabNote
from note.note_constants import SentenceNoteFields


def add_ui_action(menu: QMenu, name: str, callback: Callable[[], None]) -> None:
    menu.addAction(name, lambda: run_ui_action())

    def run_ui_action() -> None:
        callback()
        ui_utils().refresh()

def add_lookup_action_lambda(menu: QMenu, name: str, search: Callable[[],str]) -> None:
    menu.addAction(name, lookup_promise(search))

def add_lookup_action(menu: QMenu, name: str, search: str) -> None:
    menu.addAction(name, lookup_promise(lambda: search))

def add_single_vocab_lookup_action(menu: QMenu, name:str, vocab:str) -> None:
    menu.addAction(name, lookup_promise(lambda: f"{su.vocab_read} Vocab:{vocab}"))

def add_text_vocab_lookup(menu: QMenu, name:str, text:str) -> None:
    add_lookup_action_lambda(menu, name, lambda: su.text_vocab_lookup(text))

def add_vocab_dependencies_lookup(menu: QMenu, name: str, vocab: VocabNote) -> None:
    add_lookup_action_lambda(menu, name, lambda: su.vocab_dependencies_lookup_query(vocab))


def add_sentence_lookup(menu: QMenu, name: str, search: str) -> None:
    add_lookup_action(menu, name, f"(deck:*sentence* deck:*listen*) (Q:*{search}* OR Reading:*{search}* OR {su.field_contains_word(SentenceNoteFields.ParsedWords, search)})")
