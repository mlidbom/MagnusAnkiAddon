from __future__ import annotations

from typing import Callable, Generic, TypeVar

from autoslot import Slots

TValue: TypeVar = TypeVar("TValue")

class FieldWrapper(Generic[TValue], Slots):
    def __init__(self, getter: Callable[[], TValue], setter: Callable[[TValue], None], save_callback: Callable[[], None]) -> None:
        self._save: Callable[[], None] = save_callback
        self._getter = getter
        self._set_without_save = setter

    def set(self, value: TValue) -> None:
        self._set_without_save(value)
        self._save()

    def get(self) -> TValue: return self._getter()
