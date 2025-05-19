from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Generic, TypeVar

from autoslot import Slots

if TYPE_CHECKING:
    from note.notefields.json_object_field import JsonObjectField
    from sysutils.weak_ref import WeakRef
    pass

TValue: TypeVar = TypeVar("TValue")

class FieldWrapper(Generic[TValue], Slots):
    _secret = "aoeulrcaboeusthb"
    def __init__(self, getter: Callable[[], TValue], setter: Callable[[TValue], None], save_callback: Callable[[], None], secret: str) -> None:
        if FieldWrapper._secret != secret: raise ValueError("use the factory methods, not this private constructor")
        self._save_callback: Callable[[], None] = save_callback
        self._getter = getter
        self._setter = setter

    def set(self, value: TValue) -> None:
        self._setter(value)
        self._save_callback()

    def get(self) -> TValue: return self._getter()


    @classmethod
    def for_json_object_field(cls, field: WeakRef[JsonObjectField[TValue]]) -> FieldWrapper[TValue]:
        def setter(value: TValue) -> None: field().set(value)
        return cls(lambda: field().get(), setter, lambda: field().save(), FieldWrapper._secret)
