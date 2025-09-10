from __future__ import annotations

import threading
from concurrent.futures import Future
from typing import Callable, Generic, TypeVar, cast

from autoslot import Slots

T = TypeVar("T")

class Lazy(Generic[T], Slots):
    def __init__(self, factory: Callable[[], T]) -> None:
        self.factory = factory
        self._instance: T | None = None

    def instance(self) -> T:
        if self._instance is None:
            self._instance = self.factory()
        return self._instance

    def __call__(self) -> T: return self.instance()

    @classmethod
    def from_value(cls, result: T) -> Lazy[T]:
        return cls(lambda: result)

    def reset(self) -> None:
        self._instance = None

class BackgroundInitialingLazy(Generic[T], Slots):
    def __init__(self, factory: Callable[[], T], delay_seconds: float = 0) -> None:
        self._lock = threading.Lock()
        self._future_instance: Future[T] | None = None
        self._factory = factory
        if delay_seconds > 0:
            self._pending_init_timer = threading.Timer(delay_seconds, self._init)
            self._pending_init_timer.start()
        else:
            self._init()

    def _init(self) -> None:
        with self._lock:
            if not self._future_instance:
                from sysutils import app_thread_pool
                self._future_instance = app_thread_pool.pool.submit(self._factory)

    def is_initialized(self) -> bool: return bool(self._future_instance and self._future_instance.done() and not self._future_instance.cancelled())

    def try_cancel_scheduled_init(self) -> bool:
        if self._future_instance:
            return False

        self._pending_init_timer.cancel()

        return not self._future_instance

    def instance(self) -> T:
        if self.try_cancel_scheduled_init():
            self._init()

        from sysutils import app_thread_pool
        if not self.is_initialized() and app_thread_pool.current_is_ui_thread():
            from sysutils import progress_display_runner

            def init() -> None:
                cast(Future[T], self._future_instance).result()

            progress_display_runner.run_on_background_thread_with_spinning_progress_dialog("Populating cache", init)

        return cast(Future[T], self._future_instance).result()
