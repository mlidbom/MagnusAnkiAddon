from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import Tags
from note.notefields.tag_flag_field import TagFlagField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatching
    from sysutils.weak_ref import WeakRef

class RequiresCompound(TagFlagField, Slots):
    def __init__(self, matching: WeakRef[VocabNoteMatching]) -> None:
        super().__init__(matching().vocab, Tags.Vocab.Matching.Requires.compound)
        self.matching: WeakRef[VocabNoteMatching] = matching

    def set_to(self, value: bool) -> None:
        super().set_to(value)
        if value: self.matching().requires_single_token.set_to(False)
