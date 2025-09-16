from __future__ import annotations

from concurrent.futures.thread import ThreadPoolExecutor
from typing import TYPE_CHECKING

from ankiutils import app
from PyQt6.QtCore import QCoreApplication, QThread
from sysutils import ex_thread
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from collections.abc import Callable

pool = ThreadPoolExecutor()

def current_is_ui_thread() -> bool:
    return bool(QCoreApplication.instance() and non_optional(QCoreApplication.instance()).thread() == QThread.currentThread())

def run_on_ui_thread_synchronously[T](func: Callable[[], T]) -> T:
    if app.is_testing or current_is_ui_thread():
        return func()

    done_running: list[T] = []

    from aqt import mw
    mw.taskman.run_on_main(lambda: done_running.append(func()))

    while not len(done_running) > 0:
        ex_thread.sleep_thread_not_doing_the_current_work(0.001)

    return done_running[0]


def run_on_ui_thread_fire_and_forget(func: Callable[[], None]) -> None:
    if app.is_testing or current_is_ui_thread():
        func()

    return app.main_window().taskman.run_on_main(func)
