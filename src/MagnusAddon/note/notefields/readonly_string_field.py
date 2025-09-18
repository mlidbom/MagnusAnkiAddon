from __future__ import annotations

from typing import TYPE_CHECKING

from ex_autoslot import AutoSlots

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

# this class is used extremely much so its performance, and memory usage, is crucial keep that in mind when changing anything
class ReadOnlyStringField(AutoSlots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        # this method is interesting for profiling so we want a unuique name we can find in the trace
        def read_only_string_field_get_initial_value_for_caching() -> str: return note().get_field(field_name)
        self.value: str = read_only_string_field_get_initial_value_for_caching()
