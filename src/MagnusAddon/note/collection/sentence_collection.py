from __future__ import annotations

from anki.collection import Collection
from anki.notes import Note

from note.collection.backend_facade import BackEndFacade
from note.note_constants import NoteTypes
from note.sentencenote import SentenceNote

class SentenceCollection:
    def __init__(self, collection: Collection):
        def sentence_constructor(note: Note) -> SentenceNote: return SentenceNote(note)
        self.collection = BackEndFacade[SentenceNote](collection, sentence_constructor, NoteTypes.Sentence)

    def all(self) -> list[SentenceNote]: return list(self.collection.all())

    def search(self, query: str) -> list[SentenceNote]: return list(self.collection.search(query))
