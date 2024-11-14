from concurrent.futures.thread import ThreadPoolExecutor

from PyQt6.QtCore import QCoreApplication, QThread

from sysutils.typed import checked_cast, non_optional

pool = ThreadPoolExecutor()

def current_is_ui_thread() -> bool:
    return bool(QCoreApplication.instance() and non_optional(QCoreApplication.instance()).thread() == QThread.currentThread())