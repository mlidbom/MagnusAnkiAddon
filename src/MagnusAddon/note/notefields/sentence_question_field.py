from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # type: ignore[reportMissingTypeStubs]
from sysutils import ex_str
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from note.notefields.mutable_string_field import MutableStringField

class SentenceQuestionField(WeakRefable, Slots):
    word_break_tag: str = "<wbr>"
    def __init__(self, primary_field: MutableStringField, fallback_field: MutableStringField) -> None:
        self._field: MutableStringField = primary_field
        self._fallback_field: MutableStringField = fallback_field
        weakself = WeakRef(self)
        self._value: Lazy[str] = Lazy(lambda: ex_str.strip_html_markup(weakself()._sentence_question_field_raw_value().replace(self.word_break_tag, ex_str.invisible_space)))
        self._field.on_change(self._value.reset)
        self._fallback_field.on_change(self._value.reset)

    def _sentence_question_field_raw_value(self) -> str: return self._field.value or self._fallback_field.value

    def get(self) -> str: return self._value()

    def split_token_with_word_break_tag(self, section: str) -> None:
        if len(section) < 2: return
        raw_value = self._sentence_question_field_raw_value()
        new_section = f"{section[0]}{self.word_break_tag}{section[1:]}"
        new_value = raw_value.replace(section, new_section)
        self._field.set(new_value)
