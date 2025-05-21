from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from ankiutils import query_builder, search_executor
from ankiutils.app import get_ui_utils
from ankiutils.search_executor import lookup_promise
from PyQt6.QtWidgets import QMenu, QMessageBox
from ui.menus.menu_utils import shortcutfinger

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from note.vocabulary.vocabnote import VocabNote
    from PyQt6.QtGui import QAction


def _confirm(menu: QMenu, message:str) -> bool:
    message = shortcutfinger.remove_shortcut_text(message)
    return QMessageBox.question(
        menu.parentWidget(),
        f"{message}?",
        f"{message}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.Yes
    ) == QMessageBox.StandardButton.Yes

def add_ui_action(menu: QMenu, name: str, callback: Callable[[], None], enabled:bool = True, confirm:bool = False) -> QAction:
    def run_ui_action() -> None:
        if not confirm or _confirm(menu, name):
            callback()
            get_ui_utils().refresh()

    action = menu.addAction(name, lambda: run_ui_action())
    action.setEnabled(enabled)
    return action

def add_lookup_action_lambda(menu: QMenu, name: str, search: Callable[[],str]) -> None:
    menu.addAction(name, lookup_promise(search))

def add_lookup_action(menu: QMenu, name: str, search: str) -> None:
    menu.addAction(name, lookup_promise(lambda: search))

def add_single_vocab_lookup_action(menu: QMenu, name:str, vocab:str) -> None:
    menu.addAction(name, lookup_promise(lambda: query_builder.single_vocab_by_form_exact(vocab)))

def add_vocab_dependencies_lookup(menu: QMenu, name: str, vocab: VocabNote) -> None:
    add_lookup_action_lambda(menu, name, lambda: query_builder.vocab_dependencies_lookup_query(vocab))

def create_note_action(menu: QMenu, name: str, callback: Callable[[], JPNote]) -> None:
    def run_ui_action() -> None:
        new_note = callback()
        search_executor.do_lookup_and_show_previewer(query_builder.notes_lookup([new_note]))
        get_ui_utils().refresh()

    menu.addAction(name, lambda: run_ui_action())

def create_vocab_note_action(menu: QMenu, name: str, callback: Callable[[], VocabNote]) -> None:
    def do_it() -> VocabNote:
        new_note = callback()
        from batches import local_note_updater
        local_note_updater.reparse_sentences_for_vocab(new_note)
        return new_note

    create_note_action(menu, name, do_it)