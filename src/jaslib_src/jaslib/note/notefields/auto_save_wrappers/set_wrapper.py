from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from autoslot import Slots

if TYPE_CHECKING:
    from collections.abc import Callable

    from typed_linq_collections.collections.q_set import QSet

    from jaslib.note.notefields.json_object_field import MutableSerializedObjectField

# noinspection PyUnusedFunction
class FieldSetWrapper[TValue](Slots):
    _secret: str = "aoeulrcaboeusthb"
    def __init__(self, save_callback: Callable[[], None], value: Callable[[], QSet[TValue]], secret: str) -> None:
        if FieldSetWrapper._secret != secret: raise ValueError("use the factory methods, not this private constructor")
        self._save: Callable[[], None] = save_callback
        self._value: Callable[[], QSet[TValue]] = value #never replace _value or the save method will stop working...

    def get(self) -> QSet[TValue]: return self._value()
    def __call__(self) -> QSet[TValue]: return self.get()

    def add(self, value: TValue) -> None:
        self._value().add(value)
        self._save()

    def remove(self, key: TValue) -> None:
        self._value().remove(key)
        self._save()

    def discard(self, key: TValue) -> None:
        self._value().discard(key)
        self._save()

    def clear(self) -> None: self._value().clear()

    def overwrite_with(self, other: FieldSetWrapper[TValue]) -> None:
        self._value().clear()
        self._value().update(other.get())
        self._save()

    def none(self) -> bool: return not self.any()
    def any(self) -> bool: return any(self._value())

    @classmethod
    def for_json_object_field(cls, field: MutableSerializedObjectField[Any], value: QSet[TValue]) -> FieldSetWrapper[TValue]:  # pyright: ignore[reportExplicitAny]
        return FieldSetWrapper(lambda: field.save(), lambda: value, FieldSetWrapper._secret)

    @override
    def __repr__(self) -> str: return self._value().__repr__() if self._value() else "{}"
