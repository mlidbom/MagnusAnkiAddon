from __future__ import annotations

from typing import override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]


class ValueWrapper[TValue](Slots):
    def __init__(self, value: TValue) -> None:
        self._value: TValue = value

    def set(self, value: TValue) -> None:
        self._value = value

    def get(self) -> TValue:
        return self._value

    @override
    def __repr__(self) -> str: return self._value.__repr__()