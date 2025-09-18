from __future__ import annotations

from typing import TYPE_CHECKING, override

from ankiutils import app
from ankiutils.app import col
from ex_autoslot import AutoSlots

if TYPE_CHECKING:
    from note.notefields.json_object_field import MutableSerializedObjectField
    from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class SeeAlso(AutoSlots):
    def __init__(self, vocab: WeakRef[VocabNote], data: MutableSerializedObjectField[RelatedVocabData]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._data: MutableSerializedObjectField[RelatedVocabData] = data

    def strings(self) -> set[str]: return self._data.get().see_also
    def notes(self) -> list[VocabNote]:
        return col().vocab.with_any_form_in_prefer_exact_match(list(self.strings()))

    def add(self, to_add: str) -> None:
        self.strings().add(to_add)

        for added_note in app.col().vocab.with_question(to_add):
            if self._vocab().get_question() not in added_note.related_notes.see_also.strings():
                added_note.related_notes.see_also.add(self._vocab().get_question())

        self._data.save()

    def remove(self, to_remove: str) -> None:
        self.strings().remove(to_remove)

        for removed_note in app.col().vocab.with_question(to_remove):
            if self._vocab().get_question() in removed_note.related_notes.see_also.strings():
                removed_note.related_notes.see_also.remove(self._vocab().get_question())

        self._data.save()

    @override
    def __repr__(self) -> str: return self._data.__repr__()