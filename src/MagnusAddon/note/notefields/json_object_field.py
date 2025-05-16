from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from note.notefields.string_field import StringField
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

T: TypeVar = TypeVar("T")

class JsonObjectSerializer(Generic[T]):
    def serialize(self, obj: T) -> str: raise NotImplementedError()
    def deserialize(self, json: str) -> T: raise NotImplementedError()

class JsonObjectField(Generic[T]):
    def __init__(self, note: WeakRef[JPNote], field: str, serializer: JsonObjectSerializer[T]) -> None:
        self._note: WeakRef[JPNote] = note
        self._field: StringField = StringField(note, field)
        self._serializer: JsonObjectSerializer[T] = serializer
        self._value: Lazy[T] = Lazy(lambda: serializer.deserialize(self._field.get()))

    def get(self) -> T: return self._value()
    def set(self, value: T) -> None:
        self._value = Lazy.from_value(value)
        self._field.set(self._serializer.serialize(value))
