from __future__ import annotations

import time
from typing import TYPE_CHECKING, override

from autoslot import Slots
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QProgressDialog
from sysutils import timeutil

if TYPE_CHECKING:
    from collections.abc import Callable

class ITaskRunner:
    def process_with_progress[TInput, TOutput](self, items: list[TInput], process_item: Callable[[TInput], TOutput], message: str) -> list[TOutput]: raise NotImplementedError()  # pyright: ignore
    def set_label_text(self, text: str) -> None: raise NotImplementedError()  # pyright: ignore
    def close(self) -> None: raise NotImplementedError()

class TaskRunner(Slots):
    @staticmethod
    def create(window_title: str, label_text: str, visible: bool) -> ITaskRunner:
        if not visible:
            return InvisibleTaskRunner(window_title, label_text)
        return QtTaskProgressRunner(window_title, label_text)

    @staticmethod
    def invisible() -> ITaskRunner:
        return InvisibleTaskRunner("", "")

class InvisibleTaskRunner(ITaskRunner, Slots):
    def __init__(self, window_title: str, label_text: str) -> None:
        pass

    @override
    def process_with_progress[TInput, TOutput](self, items: list[TInput], process_item: Callable[[TInput], TOutput], message: str) -> list[TOutput]:
        return [process_item(item) for item in items]
    @override
    def set_label_text(self, text: str) -> None: pass
    @override
    def close(self) -> None: pass

class QtTaskProgressRunner(ITaskRunner, Slots):
    def __init__(self, window_title: str, label_text: str) -> None:
        self.dialog: QProgressDialog = QProgressDialog(f"""{window_title}...""", None, 0, 0)
        self.dialog.setWindowTitle(f"""{window_title}""")
        self.dialog.setFixedWidth(600)
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.set_label_text(label_text)
        self.dialog.setRange(0, 0)  # Indeterminate range for spinning effect
        self.dialog.show()
        QApplication.processEvents()

    @override
    def set_label_text(self, text: str) -> None:
        self.dialog.setLabelText(text)
        QApplication.processEvents()

    @override
    def process_with_progress[TInput, TOutput](self, items: list[TInput], process_item: Callable[[TInput], TOutput], message: str) -> list[TOutput]:
        total_items = len(items)
        start_time = time.time()
        results: list[TOutput] = []
        self.dialog.setRange(0, total_items + 1) # add one to keep the dialog open
        original_label = self.dialog.labelText()

        last_refresh = 0.0

        for current_item, item in enumerate(items):
            results.append(process_item(item))
            if time.time() - last_refresh > 0.3 or current_item == total_items - 1:
                last_refresh = time.time()
                self.dialog.setValue(current_item + 1)
                elapsed_time = time.time() - start_time
                if current_item > 0:
                    estimated_total_time = (elapsed_time / current_item) * total_items
                    estimated_remaining_time = estimated_total_time - elapsed_time
                    self.set_label_text(f"{message} {current_item} of {total_items} Remaining: {timeutil.format_seconds_as_hh_mm_ss(estimated_remaining_time)}")

                QApplication.processEvents()

        self.dialog.setRange(0, 0)
        self.set_label_text(original_label)
        QApplication.processEvents()

        return results
    @override
    def close(self) -> None:
        self.dialog.close()
        self.dialog.deleteLater()
