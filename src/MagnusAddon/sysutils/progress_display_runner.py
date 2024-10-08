from PyQt6.QtWidgets import QProgressDialog, QApplication
from PyQt6.QtCore import Qt
import time
from typing import Callable, List, TypeVar

from sysutils import timeutil

T = TypeVar('T')

def open_spinning_progress_dialog(message: str) -> QProgressDialog:
    progress_dialog = QProgressDialog(f"{message}", None, 0, 0)
    progress_dialog.setWindowTitle(f"{message}")
    progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
    progress_dialog.setRange(0, 0)  # Indeterminate range for spinning effect
    progress_dialog.show()

    return progress_dialog

def process_with_progress(items: List[T], process_item: Callable[[T], None], message:str, allow_cancel: bool, delay_display: bool = False) -> None:
    total_items = len(items)
    start_time = time.time()
    progress_dialog: QProgressDialog | None = None
    last_refresh = 0.0

    for current_item, item in enumerate(items):
        if not progress_dialog and (time.time() - start_time > 0.2 or not delay_display):
            progress_dialog = QProgressDialog(f"""{message}...""", "Cancel" if allow_cancel else None, 0, total_items)
            progress_dialog.setWindowTitle(f"""{message}""")
            progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)

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