from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils import ex_str
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class SentenceQuestionField(Slots):
    word_break_tag: str = "<wbr>"
    def __init__(self, note: WeakRef[JPNote], primary_field: str, fallback_field: str) -> None:
        self._note: WeakRef[JPNote] = note
        self._field: str = primary_field
        self._fallback_field: str = fallback_field
        self._value: Lazy[str] = Lazy(lambda: ex_str.strip_html_markup((note().get_field(primary_field)
                                                                        or note().get_field(fallback_field))
                                                                       .replace(self.word_break_tag, ex_str.invisible_space)))

    def get(self) -> str: return self._value()

    def split_token_with_word_break_tag(self, section: str) -> None:
        if len(section) < 2: return
        new_section = f"{section[0]}{self.word_break_tag}{section[1:]}"

        new_value = self.get().replace(section, new_section)
        note = self._note()
        if note.get_field(self._field) != "": note.set_field(self._field, new_value)
        else: note.set_field(self._fallback_field, new_value)
        self._value.reset()
