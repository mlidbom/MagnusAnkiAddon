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
    def __init__(self, factory: Callable[[], T]):
        self._instance = app_thread_pool.pool.submit(factory)

    def is_initialized(self) -> bool: return self._instance.done() and not self._instance.cancelled()

    def instance(self) -> T:
        if not self.is_initialized() and app_thread_pool.current_is_ui_thread():
            from sysutils import progress_display_runner

            def init() -> None:
                self._instance.result()

            progress_display_runner.with_spinning_progress_dialog("Populating cache", init)

        return self._instance.result()
