from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

# this field is used extremely much, so its design is crucial for both performance and memory usage, keep in mind when changing anything
# if a field is read-only, make sure to to use ReadOnlyStringField instead, which uses less memory
class MutableStringField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._note: WeakRef[JPNote] = note
        self._field_name: str = field_name

    @property
    def value(self) -> str: return self._note().get_field(self._field_name)

    def set(self, value: str) -> None: self._note().set_field(self._field_name, value)

    # noinspection PyUnusedFunction
    def empty(self) -> None: self.set("")

    def has_value(self) -> bool: return self.value != ""

    @override
    def __repr__(self) -> str: return self.value
