from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.string_field import StringField
from sysutils import ex_str

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class SentenceQuestionField(Slots):
    word_break_tag = "<wbr>"
    def __init__(self, note: WeakRef[JPNote], primary_field: str, fallback_field: str) -> None:
        self._field = StringField(note, primary_field)
        self._fallback_field = StringField(note, fallback_field)

    def _get_raw(self) -> str: return self._field.get() or self._fallback_field.get()

    def get(self) -> str: return ex_str.strip_html_markup(self._get_raw().replace(self.word_break_tag, ex_str.invisible_space))

    def split_token_with_word_break_tag(self, section: str) -> None:
        if len(section) < 2: return
        new_section = f"{section[0]}{self.word_break_tag}{section[1:]}"

        new_value = self.get().replace(section, new_section)
        if self._field.has_value(): self._field.set(new_value)
        else: self._fallback_field.set(new_value)
