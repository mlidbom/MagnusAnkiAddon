from __future__ import annotations

import time
from typing import TYPE_CHECKING, TypeVar

from autoslot import Slots
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMessageBox, QProgressDialog
from sysutils import app_thread_pool, timeutil

if TYPE_CHECKING:
    from collections.abc import Callable

T = TypeVar("T")

class Closable(Slots):
    def __init__(self, close_action: Callable[[], None]) -> None:
        self.close_action: Callable[[], None] = close_action

    def close(self) -> None: self.close_action()



def run_on_background_thread_with_spinning_progress_dialog(message:str, action: Callable[[], object]) -> None:
    dialog = _create_spinning_progress_dialog(message)

    future = app_thread_pool.pool.submit(action)

    while not future.done():
        QApplication.processEvents()
        time.sleep(0.1)

    dialog.close()


def open_spinning_progress_dialog(message: str) -> Closable:
    progress_dialog = _create_spinning_progress_dialog(message)
    QApplication.processEvents()

    def close() -> None:
        progress_dialog.close()

    return Closable(close)

def _create_spinning_progress_dialog(message: str) -> QProgressDialog:
    progress_dialog = QProgressDialog(f"{message}", None, 0, 0)
    progress_dialog.setWindowTitle(f"{message}")
    progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
    progress_dialog.setRange(0, 0)  # Indeterminate range for spinning effect
    progress_dialog.show()
    return progress_dialog

def process_with_progress(items: list[T], process_item: Callable[[T], None], message:str, allow_cancel: bool = True, display_delay_seconds: float = 0.0) -> None:
    total_items = len(items)
    start_time = time.time()
    progress_dialog: QProgressDialog | None = None
    last_refresh = 0.0

    try:

        for current_item, item in enumerate(items):
            if not progress_dialog and (time.time() - start_time >= display_delay_seconds):
                progress_dialog = QProgressDialog(f"""{message}...""", "Cancel" if allow_cancel else None, 0, total_items)
                progress_dialog.setWindowTitle(f"""{message}""")
                progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
                progress_dialog.show()

            if progress_dialog and progress_dialog.wasCanceled(): break
            process_item(item)
            if time.time() - last_refresh > 0.1 or current_item == total_items - 1:
                last_refresh = time.time()
                if progress_dialog: progress_dialog.setValue(current_item + 1)
                elapsed_time = time.time() - start_time
                if current_item > 0:
                    estimated_total_time = (elapsed_time / current_item) * total_items
                    estimated_remaining_time = estimated_total_time - elapsed_time
                    if progress_dialog: progress_dialog.setLabelText(f"{message} {current_item} of {total_items} Remaining: {timeutil.format_seconds_as_hh_mm_ss(estimated_remaining_time)}")

                QApplication.processEvents()
    finally:
        if progress_dialog: progress_dialog.close()

def show_dismissable_message(window_title: str, message:str) -> None:
    msg_box = QMessageBox()
    msg_box.setWindowTitle(window_title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()