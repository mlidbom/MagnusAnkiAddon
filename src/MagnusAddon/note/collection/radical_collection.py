from __future__ import annotations

from typing import List

from note.collection.backend_facade import BackEndFacade
from note.note_constants import NoteFields, NoteTypes
from note.radicalnote import RadicalNote

class RadicalCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection

    def by_answer(self, field_values: list[str]) -> List[RadicalNote]:
        notes = self.collection.fetch_notes_by_note_type_and_field_value(NoteTypes.Radical, NoteFields.Radical.answer, field_values)
        radical_notes = [RadicalNote(note) for note in notes]
        return radical_notes

    def all(self) -> List[RadicalNote]:
        notes = self.collection.fetch_notes_by_note_type(NoteTypes.Radical)
        radical_notes = [RadicalNote(note) for note in notes]
        return radical_notes
