from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from autoslot import Slots
from note.notefields.string_field import StringField
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRefable

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

T = TypeVar("T")

class JsonObjectSerializer(Generic[T], Slots):
    def serialize(self, obj: T) -> str: raise NotImplementedError()
    def deserialize(self, json: str) -> T: raise NotImplementedError()

class JsonObjectField(Generic[T], WeakRefable, Slots):
    def __init__(self, note: WeakRef[JPNote], field: str, serializer: JsonObjectSerializer[T]) -> None:
        self._note: WeakRef[JPNote] = note
        self._field: StringField = StringField(note, field)
        self._serializer: JsonObjectSerializer[T] = serializer
        self._value: Lazy[T] = Lazy(lambda: serializer.deserialize(self._field.get()))
        self._weakref: WeakRef[JsonObjectField[T]] | None = None

    def get(self) -> T: return self._value()
    def set(self, value: T) -> None:
        self._value = Lazy.from_value(value)
        self._field.set(self._serializer.serialize(value))

    def save(self) -> None:
        self._field.set(self._serializer.serialize(self._value()))