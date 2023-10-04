from __future__ import annotations

from typing import List

from note.collection.backend_facade import BackEndFacade
from note.kanjinote import KanjiNote
from note.note_constants import NoteFields, NoteTypes
from note.radicalnote import RadicalNote

class KanjiCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection

    def search(self, query: str) -> list[KanjiNote]:
        return [KanjiNote(note) for note in self.collection.search_notes(query)]

    def all(self) -> List[KanjiNote]:
        notes = self.collection.fetch_notes_by_note_type(NoteTypes.Kanji)
        kanji_notes = [KanjiNote(note) for note in notes]
        return kanji_notes

    def all_wani(self) -> list[KanjiNote]:
        return [kanji for kanji in self.all() if kanji.is_wani_note()]

    def by_kanji(self, field_values: list[str]) -> List[KanjiNote]:
        notes = self.collection.fetch_notes_by_note_type_and_field_value(NoteTypes.Kanji, NoteFields.Kanji.question, field_values)
        kanji_notes = [KanjiNote(note) for note in notes]
        return kanji_notes
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
