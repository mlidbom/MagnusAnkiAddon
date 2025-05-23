from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import Tags
from note.notefields.tag_flag_field import TagFlagField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class QuestionOverridesForm:
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self.tag_field: TagFlagField = TagFlagField(vocab, Tags.Vocab.question_overrides_form)

    def is_set(self) -> bool:
        return self.tag_field.is_set() # or self._vocab().matching_rules.is_strictly_suffix.is_set()
