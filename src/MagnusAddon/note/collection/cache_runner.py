from collections.abc import Callable

from aqt import qconnect
from PyQt6.QtCore import QTimer

class CacheRunner:
    def __init__(self) -> None:
        from aqt import mw
        self._updates_paused = False
        self._callbacks:list[Callable[[], None]] = []
        self._destructors: list[Callable[[], None]] = []
        self._timer = QTimer(mw)
        qconnect(self._timer.timeout, self.flush_cache_updates)

    def flush_cache_updates(self) -> None:
        if self._updates_paused: return

        for callback in self._callbacks:
            callback()

    def pause_cache_updates(self) -> None:
        self._updates_paused = True

    def resume_cache_updates(self) -> None:
        self._updates_paused = False

    def start(self) -> None:
        self._timer.start(100)  # 1000 milliseconds = 1 second

    def destruct(self) -> None:
        self._timer.stop()
        self._timer.disconnect()
        for destructor in self._destructors: destructor()

    def connect_flush_timer(self, flush_updates: Callable[[], None]) -> None:
        self._callbacks.append(flush_updates)

    def connect_destruct(self, destruct: Callable[[], None]) -> None:
        self._destructors.append(destruct)
