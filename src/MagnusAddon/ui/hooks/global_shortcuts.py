from __future__ import annotations

from aqt import gui_hooks, mw
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QWidget
from sysutils import ex_assert, typed
from sysutils.typed import checked_cast
from ui.hooks import history_navigator
from ui.open_note.open_note_dialog import NoteSearchDialog


def init() -> None:
    def bind_shortcuts(widget: QWidget) -> None:
        typed.checked_cast(pyqtBoundSignal, QShortcut(QKeySequence("Alt+Left"), widget).activated).connect(history_navigator.navigator.navigate_back)
        typed.checked_cast(pyqtBoundSignal,QShortcut(QKeySequence("Alt+Right"), widget).activated).connect(history_navigator.navigator.navigate_forward)
        typed.checked_cast(pyqtBoundSignal, QShortcut(QKeySequence("Ctrl+o"), widget).activated).connect(NoteSearchDialog.show_dialog)

    ex_assert.not_none(history_navigator.navigator, "History navigator needs to be initialized before global shortcuts are bound")
    bind_shortcuts(checked_cast(QWidget, mw))
    gui_hooks.previewer_did_init.append(bind_shortcuts)
    gui_hooks.browser_will_show.append(bind_shortcuts)
