from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.note.notefields.fallback_string_field import FallbackStringField
from sysutils import ex_str

if TYPE_CHECKING:
    from jastudio.note.notefields.mutable_string_field import MutableStringField

class StripHtmlOnReadFallbackStringField(Slots):
    def __init__(self, primary_field: MutableStringField, fallback_field: MutableStringField) -> None:
        self._field: FallbackStringField = FallbackStringField(primary_field, fallback_field)

    def get(self) -> str: return ex_str.strip_html_markup(self._field.get().replace("<wbr>", ex_str.invisible_space))
