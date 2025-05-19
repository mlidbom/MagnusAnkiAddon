from __future__ import annotations

from typing import Generic, TypeVar

from autoslot import Slots

TValue: TypeVar = TypeVar("TValue")

class ValueWrapper(Generic[TValue], Slots):
    def __init__(self, value: TValue) -> None:
        self._value = value

    def set(self, value: TValue) -> None:
        self._value = value

    def get(self) -> TValue:
        return self._value
