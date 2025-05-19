from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots

if TYPE_CHECKING:
    from note.notefields.json_object_field import JsonObjectField
    from note.vocabulary.related_notes.related_notes_data import VocabNoteRelatedNotesData
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class VocabErgativeTwin(Slots):
    def __init__(self, vocab: WeakRef[VocabNote], data: JsonObjectField[VocabNoteRelatedNotesData]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._data: JsonObjectField[VocabNoteRelatedNotesData] = data

    def get(self) -> str: return self._data.get().ergative_twin

    def set(self, value: str) -> None:
        self._data.get().ergative_twin = value

        for twin in app.col().vocab.with_question(value):
            if twin.related_notes.ergative_twin.get() != self._vocab().get_question():
                twin.related_notes.ergative_twin.set(self._vocab().get_question())
