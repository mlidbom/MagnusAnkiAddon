from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import Mine
from note.notefields.tag_flag_field import TagFlagField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class VocabNoteFlags:
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self.requires_exact_match: TagFlagField = TagFlagField(vocab(), Mine.Tags.requires_exact_match)
        self.question_overrides_form: TagFlagField = TagFlagField(vocab(),  Mine.Tags.question_overrides_form)
        self.requires_a_stem: TagFlagField = TagFlagField(vocab(),  Mine.Tags.requires_a_stem)
        self.requires_e_stem: TagFlagField = TagFlagField(vocab(),  Mine.Tags.requires_e_stem)