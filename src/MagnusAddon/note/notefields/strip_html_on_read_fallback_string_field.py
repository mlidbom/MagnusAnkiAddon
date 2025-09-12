from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.fallback_string_field import FallbackStringField
from sysutils import ex_str

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class StripHtmlOnReadFallbackStringField(Slots):
    def __init__(self, note: WeakRef[JPNote], primary_field: str, fallback_field: str) -> None:
        self._field: FallbackStringField = FallbackStringField(note, primary_field, fallback_field)

    def get(self) -> str: return ex_str.strip_html_markup(self._field.get().replace("<wbr>", ex_str.invisible_space))
