import threading
from concurrent.futures import Future
from typing import Callable, Generic, TypeVar, Optional

from sysutils import app_thread_pool

T = TypeVar('T')

class Lazy(Generic[T]):
    def __init__(self, factory: Callable[[], T]):
        self.factory = factory
        self._instance: Optional[T] = None

    def is_initialized(self) -> bool: return self._instance is not None

    def instance(self) -> T:
        if self._instance is None:
            self._instance = self.factory()
        return self._instance


class BackgroundInitialingLazy(Generic[T]):
    def __init__(self, factory: Callable[[], T], delay_seconds: float = 0):
        self._lock = threading.Lock()
        self._delay_seconds = delay_seconds
        self._instance: Optional[Future[T]] = None
        self._factory = factory
        if delay_seconds > 0:
            self._pending_init_timer = threading.Timer(1.0, self._init)
            self._pending_init_timer.start()
        else:
            self._init()

    def _init(self) -> None:
        with self._lock:
            if not self._instance:
                self._instance = app_thread_pool.pool.submit(self._factory)


    def _is_initialized(self) -> bool: return bool(self._instance and self._instance.done() and not self._instance.cancelled())

    def try_cancel_scheduled_init(self) -> bool:
        if self._instance:
            return False

        self._pending_init_timer.cancel()
        return True

    def instance(self) -> T:
        if self.try_cancel_scheduled_init():
            self._init()

        if not self._is_initialized() and app_thread_pool.current_is_ui_thread():
            from sysutils import progress_display_runner

            def init() -> None:
                self._instance.result()

            progress_display_runner.with_spinning_progress_dialog("Populating cache", init)

        return self._instance.result()
