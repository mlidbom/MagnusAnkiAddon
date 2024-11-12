from typing import Callable

from PyQt6.QtWidgets import QMenu, QMessageBox

from ankiutils import query_builder
from ankiutils.app import ui_utils
from ankiutils.search_executor import lookup_promise
from hooks import shortcutfinger
from note.vocabnote import VocabNote

def _confirm(menu: QMenu, message:str) -> bool:
    message = shortcutfinger.remove_shortcut_text(message)
    return QMessageBox.question(
        menu.parentWidget(),
        f"{message}?",
        f"{message}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.Yes
    ) == QMessageBox.StandardButton.Yes

def add_ui_action(menu: QMenu, name: str, callback: Callable[[], None], confirm:bool=False) -> None:
    def run_ui_action() -> None:
        if not confirm or _confirm(menu, name):
            callback()
            ui_utils().refresh()

    menu.addAction(name, lambda: run_ui_action())

def add_lookup_action_lambda(menu: QMenu, name: str, search: Callable[[],str]) -> None:
    menu.addAction(name, lookup_promise(search))

def add_lookup_action(menu: QMenu, name: str, search: str) -> None:
    menu.addAction(name, lookup_promise(lambda: search))

def add_single_vocab_lookup_action(menu: QMenu, name:str, vocab:str) -> None:
    menu.addAction(name, lookup_promise(lambda: query_builder.single_vocab_by_form_exact(vocab)))

def add_text_vocab_lookup(menu: QMenu, name:str, text:str) -> None:
    add_lookup_action_lambda(menu, name, lambda: query_builder.text_vocab_lookup(text))

def add_vocab_dependencies_lookup(menu: QMenu, name: str, vocab: VocabNote) -> None:
    add_lookup_action_lambda(menu, name, lambda: query_builder.vocab_dependencies_lookup_query(vocab))