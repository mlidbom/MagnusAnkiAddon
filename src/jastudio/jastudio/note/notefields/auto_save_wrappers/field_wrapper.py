from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from jastudio.note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper
    from jastudio.note.notefields.json_object_field import MutableSerializedObjectField


class FieldWrapper[TValue, TWrapper](Slots):
    def __init__(self, field: MutableSerializedObjectField[TWrapper], value: ValueWrapper[TValue]) -> None:
        self._field: MutableSerializedObjectField[TWrapper] = field
        self._value: ValueWrapper[TValue] = value

    def set(self, value: TValue) -> None:
        self._value.set(value)
        self._field.save()

    def get(self) -> TValue:
        return self._value.get()

    @override
    def __repr__(self) -> str: return self._value.__repr__()
