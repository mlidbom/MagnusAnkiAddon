from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots
from note.note_constants import Tags
from note.notefields.tag_flag_field import TagFlagField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class IsInflectingWord(TagFlagField, ProfilableAutoSlots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        super().__init__(vocab, Tags.Vocab.Matching.is_inflecting_word)
        self._vocab: WeakRef[VocabNote] = vocab

    @property
    def is_active(self) -> bool:
        return self.is_set() or self._vocab().parts_of_speech.is_inflecting_word_type()

    @override
    def __repr__(self) -> str: return f"""{self.tag}: {self.is_active}"""
