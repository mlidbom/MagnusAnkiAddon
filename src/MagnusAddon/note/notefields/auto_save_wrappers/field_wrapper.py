from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots

if TYPE_CHECKING:
    from note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper
    from note.notefields.json_object_field import MutableSerializedObjectField


class FieldWrapper[TValue, TWrapper](ProfilableAutoSlots):
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
