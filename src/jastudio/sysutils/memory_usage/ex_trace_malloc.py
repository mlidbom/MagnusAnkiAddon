from __future__ import annotations

import os
import tracemalloc

import mylog
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils import ex_gc

from jastudio.ankiutils import app


class ExMalloc(Slots):
    def __init__(self) -> None:
        self.disabled: bool = not app.config().enable_trace_malloc.get_value()
        env_override = os.environ.get("TRACEMALLOC")
        if env_override is not None:
            self.disabled = env_override != "1"

        self._last_memory: float = 0.0

    def ensure_initialized(self) -> None:
        if self.disabled: return

        if not tracemalloc.is_tracing():
            ex_gc.collect_on_ui_thread_synchronously()
            tracemalloc.start()
            mylog.info("Started tracing malloc")
            self._last_memory = tracemalloc.get_traced_memory()[0] / 1024 / 1024  # MB

    def get_memory_delta(self) -> tuple[float, float]:
        """Returns (current_mb, delta_mb) and updates last_memory"""
        if self.disabled: return 0.0, 0.0
        if not tracemalloc.is_tracing(): raise Exception("You must call ensure_initialized before calling get_memory_delta")

        ex_gc.collect_on_ui_thread_synchronously()

        current = tracemalloc.get_traced_memory()[0] / 1024 / 1024
        delta = current - self._last_memory
        self._last_memory = current
        return current, delta

    def get_memory_delta_message(self, message: str) -> str:
        if self.disabled: return ""
        current_mem, delta_mem = self.get_memory_delta()
        return f"{message}Mem: {current_mem:.1f}MB ({delta_mem:+.1f}MB)"

    def log_memory_delta(self, message: str) -> None:
        if self.disabled: return
        mylog.info(f"{message} | {self.get_memory_delta_message('')}")

    def stop(self) -> None:
        if self.disabled: return
        tracemalloc.stop()
        ex_gc.collect_on_ui_thread_synchronously()

ex_trace_malloc_instance = ExMalloc()
