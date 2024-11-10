from concurrent.futures.thread import ThreadPoolExecutor

from PyQt6.QtCore import QCoreApplication, QThread

pool = ThreadPoolExecutor()

def current_is_ui_thread() -> bool:
    return bool(QCoreApplication.instance() and QCoreApplication.instance().thread() == QThread.currentThread())