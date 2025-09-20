from __future__ import annotations

from typing import TypeVar

TValue = TypeVar("TValue", covariant=True)
TKey = TypeVar("TKey")


class KeyValuePair(tuple[TKey, TValue]):
    __slots__: tuple[str, ...] = ()
    def __new__(cls, value: tuple[TKey, TValue]):
        return super().__new__(cls, value)

    @property
    def key(self) -> TKey: return self[0]
    @property
    def value(self) -> TValue: return self[1]
