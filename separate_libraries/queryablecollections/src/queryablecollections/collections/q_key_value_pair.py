from __future__ import annotations


class KeyValuePair[TKey, TValue]:
    __slots__: tuple[str, ...] = ("_values",)
    def __init__(self, values: tuple[TKey, TValue]) -> None:
        self._values: tuple[TKey, TValue] = values

    @property
    def key(self) -> TKey: return self._values[0]
    @property
    def value(self) -> TValue: return self._values[1]
