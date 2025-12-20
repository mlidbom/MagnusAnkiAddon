from __future__ import annotations

import tracemalloc

import mylog
from ankiutils import app
from autoslot import Slots  # pyright: ignore [reportMissingTypeStubs]
from sysutils import ex_gc


class ExMalloc(Slots):
    def __init__(self) -> None:
        self._last_memory: float = 0.0

    def ensure_initialized(self) -> None:
        if not app.config().enable_trace_malloc.get_value(): return

        if not tracemalloc.is_tracing():
            ex_gc.collect_on_ui_thread_synchronously()
            tracemalloc.start()
            mylog.info("Started tracing malloc")
        self._last_memory = tracemalloc.get_traced_memory()[0] / 1024 / 1024  # MB

    def get_memory_delta(self) -> tuple[float, float]:
        """Returns (current_mb, delta_mb) and updates last_memory"""
        if not app.config().enable_trace_malloc.get_value(): return 0.0, 0.0

        ex_gc.collect_on_ui_thread_synchronously()

        current = tracemalloc.get_traced_memory()[0] / 1024 / 1024
        delta = current - self._last_memory
        self._last_memory = current
        return current, delta

    def get_memory_delta_message(self, message: str) -> str:
        if not app.config().enable_trace_malloc.get_value(): return ""
        current_mem, delta_mem = self.get_memory_delta()
        return f"{message}Mem: {current_mem:.1f}MB ({delta_mem:+.1f}MB)"

    def log_memory_delta(self, message: str) -> None:
        if not app.config().enable_trace_malloc.get_value(): return
        mylog.info(f"{message} | {self.get_memory_delta_message('')}")

ex_trace_malloc_instance = ExMalloc()
