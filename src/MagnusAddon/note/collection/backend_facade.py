from __future__ import annotations

from typing import Iterator, List, Sequence

import anki
from anki.collection import Collection
from anki.notes import Note, NoteId

from note.jpnote import JPNote
from note.note_constants import Builtin

class BackEndFacade:
    def __init__(self, anki_collection: Collection):
        self.anki_collection = anki_collection

    def with_note_type(self, note_type: str) -> Iterator[anki.notes.Note]:
        return self.search(f"{Builtin.Note}:{note_type}")

    def search(self, query: str) -> Iterator[Note]:
        return self.by_id(self.anki_collection.find_notes(query))

    def by_id(self, note_ids: Sequence[NoteId]) -> Iterator[anki.notes.Note]:
        return (self.anki_collection.get_note(note_id) for note_id in note_ids)
