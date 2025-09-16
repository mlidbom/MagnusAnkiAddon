from __future__ import annotations

import time
from typing import TYPE_CHECKING, override

import mylog
from aqt import QLabel
from autoslot import Slots
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QProgressDialog
from sysutils import app_thread_pool, ex_thread, timeutil
from sysutils.timeutil import StopWatch
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from collections.abc import Callable

class ITaskRunner:
    def process_with_progress[TInput, TOutput](self, items: list[TInput], process_item: Callable[[TInput], TOutput], message: str) -> list[TOutput]: raise NotImplementedError()  # pyright: ignore
    def set_label_text(self, text: str) -> None: raise NotImplementedError()  # pyright: ignore
    def close(self) -> None: raise NotImplementedError()
    def run_on_background_thread_with_spinning_progress_dialog[TResult](self, message: str, action: Callable[[], TResult]) -> TResult: raise NotImplementedError()  # pyright: ignore

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
    # noinspection PyUnusedLocal
    def __init__(self, window_title: str, label_text: str) -> None:  # pyright: ignore
        pass

    @override
    def process_with_progress[TInput, TOutput](self, items: list[TInput], process_item: Callable[[TInput], TOutput], message: str) -> list[TOutput]:
        result = [process_item(item) for item in items]
        total_items = len(items)
        watch = StopWatch()
        mylog.info(f"##--InvisibleTaskRunner--## Finished {message} in {watch.elapsed_formatted()} handled {total_items} items")
        return result
    @override
    def set_label_text(self, text: str) -> None: pass  # pyright: ignore
    @override
    def close(self) -> None: pass
    @override
    def run_on_background_thread_with_spinning_progress_dialog[TResult](self, message: str, action: Callable[[], TResult]) -> TResult:  # pyright: ignore
        watch = StopWatch()
        result = action()
        mylog.info(f"##--QtTaskProgressRunner--## Finished {message} in {watch.elapsed_formatted()}")
        return result

class QtTaskProgressRunner(ITaskRunner, Slots):
    def __init__(self, window_title: str, label_text: str) -> None:
        dialog = QProgressDialog(f"""{window_title}...""", None, 0, 0)
        self.dialog: QProgressDialog = dialog
        dialog.setWindowTitle(f"""{window_title}""")
        dialog.setFixedWidth(600)
        non_optional(dialog.findChild(QLabel)).setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._set_spinning_with_message(label_text)
        dialog.show()
        QApplication.processEvents()

    @override
    def set_label_text(self, text: str) -> None:
        self.dialog.setLabelText(text)
        QApplication.processEvents()

    def _set_spinning_with_message(self, message: str) -> None:
        self.dialog.setLabelText(message)
        self.dialog.setRange(0, 0)

    @override
    def run_on_background_thread_with_spinning_progress_dialog[TResult](self, message: str, action: Callable[[], TResult]) -> TResult:
        watch = StopWatch()
        self._set_spinning_with_message(message)

        future = app_thread_pool.pool.submit(action)

        while not future.done():
            QApplication.processEvents()
            ex_thread.sleep_thread_not_doing_the_current_work(0.05)

        mylog.info(f"##--QtTaskProgressRunner--## Finished {message} in {watch.elapsed_formatted()}")
        return future.result()

    @override
    def process_with_progress[TInput, TOutput](self, items: list[TInput], process_item: Callable[[TInput], TOutput], message: str) -> list[TOutput]:
        self.set_label_text(f"{message} 0 of ?? Remaining: ??")  # len may take a while so make sure we set the label first
        total_items = len(items)
        watch = StopWatch()
        start_time = time.time()
        results: list[TOutput] = []
        self.dialog.setRange(0, total_items + 1)  # add one to keep the dialog open
        original_label = self.dialog.labelText()
        self.set_label_text(f"{message} 0 of {total_items} Remaining: ??")

        last_refresh = 0.0

        for current_item, item in enumerate(items):
            results.append(process_item(item))
            if time.time() - last_refresh > 0.1 or current_item == total_items - 1:
                last_refresh = time.time()
                self.dialog.setValue(current_item + 1)
                elapsed_time = time.time() - start_time
                if current_item > 0:
                    estimated_total_time = (elapsed_time / current_item) * total_items
                    estimated_remaining_time = estimated_total_time - elapsed_time
                    self.set_label_text(f"{message} {current_item} of {total_items} Remaining: {timeutil.format_seconds_as_hh_mm_ss(estimated_remaining_time)}")

                QApplication.processEvents()

        mylog.info(f"##--QtTaskProgressRunner--## Finished {message} in {watch.elapsed_formatted()} handled {total_items} items")

        self.dialog.setRange(0, 0)
        self.set_label_text(original_label)
        QApplication.processEvents()

        return results
    @override
    def close(self) -> None:
        self.dialog.close()
        self.dialog.deleteLater()
