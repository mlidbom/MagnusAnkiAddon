from __future__ import annotations

from typing import Callable, Generic, Iterator, Sequence, TypeVar

import anki
from anki.collection import Collection
from anki.notes import Note, NoteId

from note.jpnote import JPNote
from note.note_constants import Builtin

TNote = TypeVar('TNote', bound=JPNote)

class BackEndFacade(Generic[TNote]):
    def __init__(self, anki_collection: Collection, constructor: Callable[[Note], TNote], note_type: str):
        self.anki_collection = anki_collection
        self.constructor = constructor
        self.note_type = note_type

    def all(self) -> Iterator[TNote]:
        return self.search(f"{Builtin.Note}:{self.note_type}")

    def search(self, query: str) -> Iterator[TNote]:
        return self.by_id(self.anki_collection.find_notes(query))

    def by_id(self, note_ids: Sequence[NoteId]) -> Iterator[TNote]:
        return (self.constructor(self.anki_collection.get_note(note_id)) for note_id in note_ids)
