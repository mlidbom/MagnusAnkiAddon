from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # type: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

# this field is used extremely much, so its design is crucial for both performance and memory usage, keep in mind when changing anything
# if a field is read-only, make sure to to use ReadOnlyStringField instead, which uses less memory
class ReadonlyStringField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._value: str = note().get_field(field_name)

    @property
    def value(self) -> str: return self._value

    def has_value(self) -> bool: return self.value != ""

    @override
    def __repr__(self) -> str: return self.value
