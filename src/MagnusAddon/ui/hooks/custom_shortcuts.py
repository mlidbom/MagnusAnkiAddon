from __future__ import annotations

from typing import Callable, TypeVar

import aqt
from ankiutils import app, ui_utils
from aqt import gui_hooks, mw
from note.kanjinote import KanjiNote
from note.sentences.sentencenote import SentenceNote
from note.vocabulary.vocabnote import VocabNote
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QWidget
from sysutils import ex_assert, typed
from sysutils.typed import checked_cast, try_cast
from ui.hooks import history_navigator
from ui.open_note.open_note_dialog import NoteSearchDialog

T: TypeVar = TypeVar("T")

def init() -> None:
    def try_get_review_note_of_type(note_type: type[T]) -> T | None:
        return try_cast(note_type, ui_utils.try_get_review_note())

    def remove_mnemonic() -> None:
        kanji = try_get_review_note_of_type(KanjiNote)
        if kanji:
            kanji.set_user_mnemonic("")
            app.get_ui_utils().refresh()

        vocab = try_get_review_note_of_type(VocabNote)
        if vocab:
            vocab.user.mnemonic.empty()
            app.get_ui_utils().refresh()

    def generate_compound_parts() -> None:
        vocab = try_get_review_note_of_type(VocabNote)
        if vocab:
            vocab.compound_parts.auto_generate()
            app.get_ui_utils().refresh()

    def reset_incorrect_matches() -> None:
        sentence = try_get_review_note_of_type(SentenceNote)
        if sentence:
            sentence.configuration.incorrect_matches.reset()
            app.get_ui_utils().refresh()

    def reset_source_comments() -> None:
        sentence = try_get_review_note_of_type(SentenceNote)
        if sentence:
            sentence.source_comments.empty()
            app.get_ui_utils().refresh()

    def inject_shortcuts(_state: aqt.main.MainWindowState, shortcuts:list[tuple[str, Callable]]) -> None:
        def remove_shortcut(string: str) -> None:
            for shortcut in shortcuts:
                if shortcut[0] == string:
                    shortcuts.remove(shortcut)

        for char in ["0", "9", "8", "7", "u"]:
            remove_shortcut(char)

        shortcuts.append(("0", remove_mnemonic))
        shortcuts.append(("9", generate_compound_parts))
        shortcuts.append(("8", reset_incorrect_matches))
        shortcuts.append(("7", reset_source_comments))

    def bind_shortcuts(widget: QWidget) -> None:
        typed.checked_cast(pyqtBoundSignal, QShortcut(QKeySequence("Alt+Left"), widget).activated).connect(history_navigator.navigator.navigate_back)
        typed.checked_cast(pyqtBoundSignal,QShortcut(QKeySequence("Alt+Right"), widget).activated).connect(history_navigator.navigator.navigate_forward)
        typed.checked_cast(pyqtBoundSignal, QShortcut(QKeySequence("Ctrl+o"), widget).activated).connect(NoteSearchDialog.show_dialog)

    ex_assert.not_none(history_navigator.navigator, "History navigator needs to be initialized before global shortcuts are bound")
    bind_shortcuts(checked_cast(QWidget, mw))
    gui_hooks.previewer_did_init.append(bind_shortcuts)
    gui_hooks.browser_will_show.append(bind_shortcuts)



    gui_hooks.state_shortcuts_will_change.append(inject_shortcuts)
