from __future__ import annotations

from typing import TYPE_CHECKING

import aqt
from jaslib.sysutils.typed import checked_cast
from jastudio.ankiutils import app
from jastudio.sysutils import ex_gc
from PyQt6.QtCore import pyqtBoundSignal

if TYPE_CHECKING:
    from aqt.main import AnkiQt
    from PyQt6.QtWidgets import QDialog

def noop_gc_on_dialog_finish(_self: AnkiQt, dialog: QDialog) -> None:
    # Fix anki hanging for several seconds every time a window closes
    checked_cast(pyqtBoundSignal, dialog.finished).connect(dialog.deleteLater)  # pyright: ignore[reportUnknownMemberType]
    app.get_ui_utils().tool_tip("prevented window close garbage collection", 6000)

def noop_gc_now(_self: AnkiQt) -> None:
    app.get_ui_utils().tool_tip("prevented periodic garbage collection", 6000)

def visible_garbage_collection(_self: AnkiQt) -> None:
    if (not app.config().enable_automatic_garbage_collection.get_value()
            and app.is_initialized()):
        ex_gc.collect_on_ui_thread_and_display_message("Garbage collection triggered by anki internal code")

def init() -> None:
    if app.config().prevent_anki_from_garbage_collecting_every_time_a_window_closes.get_value():
        aqt.main.AnkiQt.garbage_collect_on_dialog_finish = noop_gc_on_dialog_finish  # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

    if app.config().disable_all_automatic_garbage_collection.get_value():
        aqt.main.AnkiQt.garbage_collect_now = noop_gc_now  # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    else:
        aqt.main.AnkiQt.garbage_collect_now = visible_garbage_collection  # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
