from __future__ import annotations

from typing import List

from note.collection.backend_facade import BackEndFacade
from note.note_constants import NoteTypes
from note.vocabnote import VocabNote

class VocabCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection

    def search(self, query: str) -> list[VocabNote]:
        return [VocabNote(note) for note in (self.collection.search_notes(query))]

    def all_wani(self) -> List[VocabNote]:
        notes = self.collection.fetch_notes_by_note_type(NoteTypes.Vocab)
        vocab_notes = [VocabNote(note) for note in notes]
        vocab_notes = [vocab for vocab in vocab_notes if vocab.is_wani_note()]
        return vocab_notes

    def all(self) -> List[VocabNote]:
        notes = self.collection.fetch_notes_by_note_type(NoteTypes.Vocab)
        vocab_notes = [VocabNote(note) for note in notes]
        return vocab_notes
