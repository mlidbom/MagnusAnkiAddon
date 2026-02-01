from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.note.notefields.tag_flag_field import TagFlagField
from jaslib.note.tags import Tags

if TYPE_CHECKING:
    from jaslib.note.vocabulary.vocabnote import VocabNote
    from jaslib.sysutils.weak_ref import WeakRef

class IsInflectingWord(TagFlagField, Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        super().__init__(vocab, Tags.Vocab.Matching.is_inflecting_word)
        self._vocab: WeakRef[VocabNote] = vocab

    @property
    def is_active(self) -> bool: return self.is_set() or self._vocab().parts_of_speech.is_inflecting_word_type()

    @override
    def __repr__(self) -> str: return f"""{self.tag}: {self.is_active}"""
