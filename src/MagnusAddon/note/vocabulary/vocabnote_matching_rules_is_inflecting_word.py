from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.note_constants import Tags
from note.notefields.tag_flag_field import TagFlagField
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class IsInflectingWord(TagFlagField, Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        super().__init__(vocab, Tags.Vocab.Matching.is_inflecting_word)
        self._vocab: WeakRef[VocabNote] = vocab
        self._is_active: Lazy[bool] = Lazy(lambda: self.is_set() or self._vocab().parts_of_speech.is_inflecting_word_type())

    @property
    def is_active(self) -> bool: return self._is_active()

    @override
    def __repr__(self) -> str: return f"""{self.tag}: {self.is_active}"""
