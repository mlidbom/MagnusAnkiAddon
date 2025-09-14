from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.string_field import StringField
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from note.jpnote import JPNote

class ObjectSerializer[T](Slots):
    def serialize(self, instance: T) -> str: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def deserialize(self, serialized: str) -> T: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]

class SerializedObjectField[T](WeakRefable, Slots):
    def __init__(self, note: WeakRef[JPNote], field: str, serializer: ObjectSerializer[T]) -> None:
        self._note: WeakRef[JPNote] = note
        self._field: StringField = StringField(note, field)
        self._serializer: ObjectSerializer[T] = serializer
        weakrefthis = WeakRef(self)
        self._value: Lazy[T] = Lazy(lambda: serializer.deserialize(weakrefthis()._field.get()))

    def get(self) -> T: return self._value()
    def set(self, value: T) -> None:
        self._value = Lazy[T].from_value(value)
        self._field.set(self._serializer.serialize(value))

    def save(self) -> None:
        self._field.set(self._serializer.serialize(self._value()))