from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from autoslot import Slots
from note.notefields.string_field import AutoStrippingStringField
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRefable

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

T = TypeVar("T")

class ObjectSerializer(Generic[T], Slots):
    def serialize(self, instance: T) -> str: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def deserialize(self, serialized: str) -> T: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]

class SerializedObjectField(Generic[T], WeakRefable, Slots):
    def __init__(self, note: WeakRef[JPNote], field: str, serializer: ObjectSerializer[T]) -> None:
        self._note: WeakRef[JPNote] = note
        self._field: AutoStrippingStringField = AutoStrippingStringField(note, field)
        self._serializer: ObjectSerializer[T] = serializer
        self._value: Lazy[T] = Lazy(lambda: serializer.deserialize(self._field.get()))
        self._weakref: WeakRef[SerializedObjectField[T]] | None = None

    def get(self) -> T: return self._value()
    def set(self, value: T) -> None:
        self._value = Lazy.from_value(value)
        self._field.set(self._serializer.serialize(value))

    def save(self) -> None:
        self._field.set(self._serializer.serialize(self._value()))