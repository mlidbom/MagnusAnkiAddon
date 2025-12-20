from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import AutoSlots
from note.notefields.mutable_string_field import MutableStringField
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from note.jpnote import JPNote

class ObjectSerializer[T](AutoSlots):
    def serialize(self, instance: T) -> str: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def deserialize(self, serialized: str) -> T: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]

class MutableSerializedObjectField[T](WeakRefable, AutoSlots):
    def __init__(self, note: WeakRef[JPNote], field: str, serializer: ObjectSerializer[T]) -> None:
        self._note: WeakRef[JPNote] = note
        self._field: MutableStringField = MutableStringField(note, field)
        self._serializer: ObjectSerializer[T] = serializer
        weakrefthis = WeakRef(self)
        string_field = weakrefthis()._field
        self._value: Lazy[T] = Lazy(lambda: serializer.deserialize(string_field.value))

    def get(self) -> T: return self._value()
    def set(self, value: T) -> None:
        self._value = Lazy[T].from_value(value)
        self._field.set(self._serializer.serialize(value))

    def save(self) -> None:
        self._field.set(self._serializer.serialize(self._value()))

    @override
    def __repr__(self) -> str: return self.get().__repr__()
