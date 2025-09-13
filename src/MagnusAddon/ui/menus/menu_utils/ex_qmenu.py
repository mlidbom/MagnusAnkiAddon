from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app, query_builder, search_executor
from ankiutils.app import get_ui_utils
from ankiutils.search_executor import lookup_promise
from aqt import pyqtBoundSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QMessageBox
from sysutils.typed import checked_cast, non_optional
from ui.menus.menu_utils import shortcutfinger

if TYPE_CHECKING:
    from collections.abc import Callable

    from configuration.configuration_value import ConfigurationValueBool
    from note.jpnote import JPNote
    from note.vocabulary.vocabnote import VocabNote

def build_checkbox_config_section_menu(menu: QMenu, toggles: list[ConfigurationValueBool]) -> None:
    for index, toggle in enumerate(toggles):
        add_checkbox_config(menu, toggle, shortcutfinger.finger_by_priority_order(index, toggle.title))

def add_checkbox_config(menu: QMenu, config_value: ConfigurationValueBool, _title: str) -> None:
    checkbox_action = QAction(_title, app.main_window())
    checkbox_action.setCheckable(True)
    checkbox_action.setChecked(config_value.get_value())

    config_value.on_change(checkbox_action.setChecked)  # when the value changes through another mechanism, make sure the menu changes state

    def set_value(value: bool) -> None:
        config_value.set_value(value)
        app.get_ui_utils().refresh()

    checked_cast(pyqtBoundSignal, checkbox_action.triggered).connect(set_value)  # pyright: ignore[reportUnknownMemberType]
    menu.addAction(checkbox_action)  # pyright: ignore[reportUnknownMemberType]

def _confirm(menu: QMenu, message: str) -> bool:
    message = shortcutfinger.remove_shortcut_text(message)
    return QMessageBox.question(
        menu.parentWidget(),
        f"{message}?",
        f"{message}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.Yes
    ) == QMessageBox.StandardButton.Yes

def add_ui_action(menu: QMenu, name: str, callback: Callable[[], None], enabled: bool = True, confirm: bool = False) -> QAction:
    def run_ui_action() -> None:
        if not confirm or _confirm(menu, name):
            callback()
            get_ui_utils().refresh()

    action = non_optional(menu.addAction(name, lambda: run_ui_action()))  # pyright: ignore[reportUnknownMemberType]
    action.setEnabled(enabled)
    return action

def add_lookup_action_lambda(menu: QMenu, name: str, search: Callable[[], str]) -> None:
    menu.addAction(name, lookup_promise(search))  # pyright: ignore[reportUnknownMemberType]

def add_lookup_action(menu: QMenu, name: str, search: str) -> None:
    menu.addAction(name, lookup_promise(lambda: search))  # pyright: ignore[reportUnknownMemberType]

def add_single_vocab_lookup_action(menu: QMenu, name: str, vocab: str) -> None:
    menu.addAction(name, lookup_promise(lambda: query_builder.single_vocab_by_form_exact(vocab)))  # pyright: ignore[reportUnknownMemberType]

def add_vocab_dependencies_lookup(menu: QMenu, name: str, vocab: VocabNote) -> None:
    add_lookup_action_lambda(menu, name, lambda: query_builder.vocab_dependencies_lookup_query(vocab))

def create_note_action(menu: QMenu, name: str, callback: Callable[[], JPNote]) -> None:
    def run_ui_action() -> None:
        new_note = callback()
        search_executor.do_lookup_and_show_previewer(query_builder.notes_lookup([new_note]))
        get_ui_utils().refresh()

    menu.addAction(name, lambda: run_ui_action())  # pyright: ignore[reportUnknownMemberType]

def create_vocab_note_action(menu: QMenu, name: str, callback: Callable[[], VocabNote]) -> None:
    def do_it() -> VocabNote:
        new_note = callback()
        from batches import local_note_updater
        local_note_updater.reparse_sentences_for_vocab(new_note)
        return new_note

    create_note_action(menu, name, do_it)
