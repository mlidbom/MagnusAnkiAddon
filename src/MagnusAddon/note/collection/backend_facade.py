from __future__ import annotations

from typing import TYPE_CHECKING, final

from autoslot import Slots
from note.jpnote import JPNote
from note.note_constants import Builtin

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from anki.collection import Collection
    from anki.notes import Note, NoteId

@final
class BackEndFacade[TNote: JPNote](Slots):
    def __init__(self, anki_collection: Collection, constructor: Callable[[Note], TNote], note_type: str) -> None:
        self.anki_collection = anki_collection
        self.constructor = constructor
        self.note_type = note_type

    def all(self) -> Sequence[TNote]:
        return self.search(f"{Builtin.Note}:{self.note_type}")

    # noinspection PySameParameterValue
    def search(self, query: str) -> Sequence[TNote]:
        return self.by_id(self.anki_collection.find_notes(query))

    def by_id(self, note_ids: Sequence[NoteId]) -> Sequence[TNote]:
        return [self.constructor(self.anki_collection.get_note(note_id)) for note_id in note_ids]
