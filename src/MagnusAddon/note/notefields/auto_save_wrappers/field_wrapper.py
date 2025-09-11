from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from autoslot import Slots

if TYPE_CHECKING:
    from note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper
    from note.notefields.json_object_field import SerializedObjectField

TValue = TypeVar("TValue")
TWrapper = TypeVar("TWrapper")

class FieldWrapper(Generic[TValue], Slots):
    def __init__(self, field: SerializedObjectField[TWrapper], value: ValueWrapper[TValue]) -> None:
        self._field: SerializedObjectField[TWrapper] = field
        self._value = value

    def set(self, value: TValue) -> None:
        self._value.set(value)
        self._field.save()

    def get(self) -> TValue:
        return self._value.get()