from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

if TYPE_CHECKING:
    from collections.abc import Callable

class Lazy[T](Slots):
    def __init__(self, factory: Callable[[], T]) -> None:
        self.factory: Callable[[], T] = factory
        self._instance: T | None = None

    def _lazy_get_instance(self) -> T:
        if self._instance is None:
            self._instance = self.factory()
        return self._instance

    def __call__(self) -> T: return self._lazy_get_instance()

    @staticmethod
    def from_value(result: T) -> Lazy[T]:
        return Lazy[T](lambda: result)

    def reset(self) -> None:
        self._instance = None
