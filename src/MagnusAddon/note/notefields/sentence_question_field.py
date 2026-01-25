from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils import ex_str

if TYPE_CHECKING:
    from note.notefields.mutable_string_field import MutableStringField


class SentenceQuestionField(Slots):
    word_break_tag: str = "<wbr>"
    def __init__(self, primary_field: MutableStringField, fallback_field: MutableStringField) -> None:
        self._field: MutableStringField = primary_field
        self._fallback_field: MutableStringField = fallback_field

    def _sentence_question_field_raw_value(self) -> str: return self._field.value or self._fallback_field.value

    def with_invisible_space(self) -> str: return ex_str.strip_html_markup(self._sentence_question_field_raw_value().replace(self.word_break_tag, ex_str.invisible_space))
    def without_invisible_space(self) -> str: return self.with_invisible_space().replace(ex_str.invisible_space, "")

    def split_token_with_word_break_tag(self, section: str) -> None:
        if len(section) < 2: return
        raw_value = self._sentence_question_field_raw_value()
        new_section = f"{section[0]}{self.word_break_tag}{section[1:]}"
        new_value = raw_value.replace(section, new_section)
        self._field.set(new_value)
