from __future__ import annotations

import time
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QProgressDialog
from sysutils import timeutil

if TYPE_CHECKING:
    from sysutils.standard_type_aliases import Action1

def process_with_progress[T](items: list[T], process_item: Action1[T], message: str, allow_cancel: bool = True, display_delay_seconds: float = 0.0) -> None:
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
