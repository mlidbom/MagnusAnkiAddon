from __future__ import annotations

from autoslot import Slots


class ValueWrapper[TValue](Slots):
    def __init__(self, value: TValue) -> None:
        self._value: TValue = value

    def set(self, value: TValue) -> None:
        self._value = value

    def get(self) -> TValue:
        return self._value
