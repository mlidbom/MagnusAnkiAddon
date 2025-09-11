from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar

from autoslot import Slots

if TYPE_CHECKING:
    from note.notefields.json_object_field import SerializedObjectField

TValue = TypeVar("TValue")

class FieldSetWrapper(Generic[TValue], Slots):
    _secret = "aoeulrcaboeusthb"
    def __init__(self, save_callback: Callable[[], None], value: Callable[[], set[TValue]], secret: str) -> None:
        if FieldSetWrapper._secret != secret: raise ValueError("use the factory methods, not this private constructor")
        self._save: Callable[[], None] = save_callback
        self._value: Callable[[], set[TValue]] = value #never replace _value or the save method will stop working...

    def get(self) -> set[TValue]: return self._value()

    def add(self, value: TValue) -> None:
        self._value().add(value)
        self._save()

    def remove(self, key: TValue) -> None:
        self._value().remove(key)
        self._save()

    def overwrite_with(self, other: FieldSetWrapper[TValue]) -> None:
        self._value().clear()
        self._value().update(other.get())
        self._save()

    def none(self) -> bool: return not self.any()
    def any(self) -> bool: return any(self._value())

    @classmethod
    def for_json_object_field(cls, field: SerializedObjectField[Any], value: set[TValue]) -> FieldSetWrapper[TValue]:
        return cls(lambda: field.save(), lambda: value, FieldSetWrapper._secret)

    def __repr__(self) -> str: return self._value().__repr__() if self._value() else "{}"
