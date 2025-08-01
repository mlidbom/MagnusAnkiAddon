import aqt
from PyQt6.QtWidgets import QDialog
from aqt import qconnect

def noop_gc_on_dialog_finish(self:aqt.main.AnkiQt, dialog: QDialog) -> None:
    # Fix anki hanging for several seconds every time a window closes
    qconnect(dialog.finished, lambda: dialog.deleteLater())

def init() -> None:
    aqt.main.AnkiQt.garbage_collect_on_dialog_finish = noop_gc_on_dialog_finish  # type: ignore
