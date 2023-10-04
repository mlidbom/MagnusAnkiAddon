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

    def fetch_notes_by_note_type_and_field_value(self, note_type: str, field: str,
                                                 field_values: list[str]) -> List[anki.notes.Note]:
        note_ids = self.anki_collection.find_notes(f"""{Builtin.Note}:{note_type} ( {" OR ".join( [f'{field}:"{field_value}"' for field_value in field_values] ) } )""")
        notes = self._fetch_notes_by_id(note_ids)
        return list(notes)

    def fetch_notes_by_note_type(self, note_type: str) -> Iterator[anki.notes.Note]:
        return self.search_notes(f"{Builtin.Note}:{note_type}")

    def search_notes(self, query: str) -> Iterator[Note]:
        return self._fetch_notes_by_id(self.anki_collection.find_notes(query))

    def _fetch_notes_by_id(self, note_ids: Sequence[NoteId]) -> Iterator[anki.notes.Note]:
        return (self.anki_collection.get_note(note_id) for note_id in note_ids)

    def unsuspend_note_cards(self, note: JPNote, name: str) -> None:
        print("Unsuspending {}: {}".format(JPNote.get_note_type_name(note), name))
        self.anki_collection.sched.unsuspend_cards(note.card_ids())
