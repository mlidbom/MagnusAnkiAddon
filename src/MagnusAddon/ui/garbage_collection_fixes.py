import gc

import aqt
from PyQt6.QtWidgets import QDialog
from aqt import qconnect

from ankiutils import app

def noop_gc_on_dialog_finish(self:aqt.main.AnkiQt, dialog: QDialog) -> None:
    # Fix anki hanging for several seconds every time a window closes
    qconnect(dialog.finished, lambda: dialog.deleteLater())

def visible_garbage_collection(self:aqt.main.AnkiQt) -> None:
    app.get_ui_utils().tool_tip("running garbage collection")
    gc.collect()

def init() -> None:
    aqt.main.AnkiQt.garbage_collect_on_dialog_finish = noop_gc_on_dialog_finish  # type: ignore
    aqt.main.AnkiQt.garbage_collect_now = visible_garbage_collection  # type: ignore
