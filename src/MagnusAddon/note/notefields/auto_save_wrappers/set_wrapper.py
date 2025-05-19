from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar

from autoslot import Slots

if TYPE_CHECKING:
    from note.notefields.json_object_field import JsonObjectField

TValue: TypeVar = TypeVar("TValue")

class FieldSetWrapper(Generic[TValue], Slots):
    _secret = "aoeulrcaboeusthb"
    def __init__(self, save_callback: Callable[[], None], value: set[TValue], secret:str) -> None:
        if FieldSetWrapper._secret != secret: raise ValueError("use the factory methods, not this private constructor")
        self._save: Callable[[], None] = save_callback
        self._value: set[TValue] = value

    def get(self) -> set[TValue]: return self._value

    def add(self, value: TValue) -> None:
        self._value.add(value)
        self._save()

    def remove(self, key: TValue) -> None:
        self._value.remove(key)
        self._save()

    def is_empty(self) -> bool: return len(self._value) == 0

    @classmethod
    def for_json_object_field(cls, field: JsonObjectField[Any], value: set[TValue]) -> FieldSetWrapper[TValue]:
        return cls(lambda: field.save(), value, FieldSetWrapper._secret)
