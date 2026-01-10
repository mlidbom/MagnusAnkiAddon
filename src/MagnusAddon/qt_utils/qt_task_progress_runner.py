from __future__ import annotations

import gc
import time
from typing import TYPE_CHECKING, override

import mylog
from ankiutils import app
from autoslot import Slots
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QProgressDialog
from qt_utils.i_task_progress_runner import ITaskRunner
from sysutils import app_thread_pool, ex_thread, timeutil
from sysutils.memory_usage.ex_trace_malloc import ex_trace_malloc_instance
from sysutils.timeutil import StopWatch
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from collections.abc import Callable

class QtTaskProgressRunner(ITaskRunner, Slots):
    def __init__(self, window_title: str, label_text: str, allow_cancel: bool = True, modal: bool = True) -> None:
        self.allow_cancel: bool = allow_cancel
        dialog = QProgressDialog(f"""{window_title}...""", "Cancel" if allow_cancel else None, 0, 0)
        self.dialog: QProgressDialog = dialog
        dialog.setWindowTitle(f"""{window_title}""")
        dialog.setFixedWidth(600)
        non_optional(dialog.findChild(QLabel)).setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        if modal:
            dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._set_spinning_with_message(label_text)
        dialog.show()
        QApplication.processEvents()

    # noinspection PyUnusedFunction
    @override
    def is_hidden(self) -> bool: return False

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
        QApplication.processEvents()

        future = app_thread_pool.pool.submit(action)
        while not future.done():
            QApplication.processEvents()
            ex_thread.sleep_thread_not_doing_the_current_work(0.05)

        # make sure we are done before logging, and that we have done what we can to ensure gc can run efficiently
        result = future.result()
        # noinspection PyUnusedLocal
        future = None

        mylog.info(f"##--QtTaskProgressRunner--## Finished {message} in {watch.elapsed_formatted()}{ex_trace_malloc_instance.get_memory_delta_message(' | ')}")
        return result

    @override
    def run_gc(self) -> None:
        old_label = self.dialog.labelText()
        self.run_on_background_thread_with_spinning_progress_dialog("Running garbage collection", lambda: app_thread_pool.run_on_ui_thread_synchronously(lambda: gc.collect()))
        self.set_label_text(old_label)

    @override
    def process_with_progress[TInput, TOutput](self, items: list[TInput], process_item: Callable[[TInput], TOutput], message: str, run_gc: bool = False, minimum_items_to_gc: int = 0) -> list[TOutput]:
        self.set_label_text(f"{message} 0 of ?? Remaining: ??")  # len may take a while so make sure we set the label first
        total_items = len(items)

        run_gc = run_gc and total_items >= minimum_items_to_gc
        if run_gc: self.run_gc()

        watch = StopWatch()
        start_time = time.time()
        results: list[TOutput] = []

        self.dialog.setRange(0, total_items + 1)  # add one to keep the dialog open
        original_label = self.dialog.labelText()
        self.set_label_text(f"{message} 0 of {total_items} Remaining: ??")

        last_refresh = 0.0

        for current_item, item in enumerate(items):
            results.append(process_item(item))
            if self.allow_cancel and self.dialog.wasCanceled(): break
            if time.time() - last_refresh > 0.1 or current_item == total_items - 1:
                last_refresh = time.time()
                self.dialog.setValue(current_item + 1)
                elapsed_time = time.time() - start_time
                if current_item > 0:
                    estimated_total_time = (elapsed_time / current_item) * total_items
                    estimated_remaining_time = estimated_total_time - elapsed_time
                    self.set_label_text(f"{message} {current_item} of {total_items} Total: {timeutil.format_seconds_as_hh_mm_ss(estimated_total_time)} Elapsed: {timeutil.format_seconds_as_hh_mm_ss(elapsed_time)} Remaining: {timeutil.format_seconds_as_hh_mm_ss(estimated_remaining_time)}")

                QApplication.processEvents()

        self.set_label_text(original_label)
        self.dialog.setRange(0, 0)
        QApplication.processEvents()

        # noinspection PyUnusedLocal
        items = []  # Make the garbage collection happening on the next line able to get rid of the items
        mylog.info(f"##--QtTaskProgressRunner--## Finished {message} in {watch.elapsed_formatted()} handled {total_items} items{ex_trace_malloc_instance.get_memory_delta_message(' | ')}")
        if run_gc: self.run_gc()
        return results

    @override
    def close(self) -> None:
        self.dialog.close()
        self.dialog.deleteLater()
        app.get_ui_utils().refresh()
