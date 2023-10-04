from __future__ import annotations

from note.collection.backend_facade import BackEndFacade
from note.note_constants import NoteTypes
from note.sentencenote import SentenceNote

class SentenceCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection

    def all(self) -> list[SentenceNote]:
        return [SentenceNote(note) for note in self.collection.fetch_notes_by_note_type(NoteTypes.Sentence)]

    def search(self, query: str) -> list[SentenceNote]:
        return [SentenceNote(note) for note in self.collection.search_notes(query)]
