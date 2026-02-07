from __future__ import annotations

from typing import TYPE_CHECKING

import aqt
from jaspythonutils.sysutils.typed import checked_cast
from PyQt6.QtCore import pyqtBoundSignal

from jastudio.ankiutils import app
from jastudio.sysutils import ex_gc

if TYPE_CHECKING:
    from aqt.main import AnkiQt
    from PyQt6.QtWidgets import QDialog

# noinspection Annotator
def noop_gc_on_dialog_finish(_self: AnkiQt, dialog: QDialog) -> None:  # pyright: ignore
    # Fix anki hanging for several seconds every time a window closes
    checked_cast(pyqtBoundSignal, dialog.finished).connect(dialog.deleteLater)  # pyright: ignore[reportUnknownMemberType]
    app.get_ui_utils().tool_tip("prevented window close garbage collection", 6000)

# noinspection Annotator
def noop_gc_now(_self: AnkiQt) -> None:
    app.get_ui_utils().tool_tip("prevented periodic garbage collection", 6000)

# noinspection Annotator
def visible_garbage_collection(_self: AnkiQt) -> None:
    if (not app.config().EnableAutomaticGarbageCollection.GetValue()
            and app.is_initialized()):
        ex_gc.collect_on_ui_thread_and_display_message("Garbage collection triggered by anki internal code")

def init() -> None:
    if app.config().PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses.GetValue():
        aqt.main.AnkiQt.garbage_collect_on_dialog_finish = noop_gc_on_dialog_finish  # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

    if app.config().DisableAllAutomaticGarbageCollection.GetValue():
        aqt.main.AnkiQt.garbage_collect_now = noop_gc_now  # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    else:
        aqt.main.AnkiQt.garbage_collect_now = visible_garbage_collection  # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
