from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

from jastudio.note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from jastudio.note.jpnote import JPNote
    from jastudio.sysutils.weak_ref import WeakRef

class ObjectSerializer[T](Slots):
    def serialize(self, instance: T) -> str: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def deserialize(self, serialized: str) -> T: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]

class MutableSerializedObjectField[T](Slots):
    def __init__(self, note: WeakRef[JPNote], field: str, serializer: ObjectSerializer[T]) -> None:
        self._note: WeakRef[JPNote] = note
        self._serializer: ObjectSerializer[T] = serializer
        self._field: MutableStringField = MutableStringField(note, field)
        self._value: T = serializer.deserialize(self._field.value)

    def get(self) -> T: return self._value
    def set(self, value: T) -> None:
        self._value = value
        self._field.set(self._serializer.serialize(value))

    def save(self) -> None:
        self._field.set(self._serializer.serialize(self._value))

    @override
    def __repr__(self) -> str: return self.get().__repr__()
