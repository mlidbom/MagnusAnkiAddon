from __future__ import annotations
from typing import Iterator, List, Sequence

import anki
from anki.collection import Collection

from anki.notes import NoteId, Note
from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.radicalnote import RadicalNote
from note.vocabnote import VocabNote
from note.kanjinote import KanjiNote
from note.note_constants import NoteFields, NoteTypes, Builtin
from sysutils import listutils


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

class SentenceCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection

    def all(self) -> list[SentenceNote]:
        return [SentenceNote(note) for note in self.collection.fetch_notes_by_note_type(NoteTypes.Sentence)]

    def search(self, query: str) -> list[SentenceNote]:
        return [SentenceNote(note) for note in self.collection.search_notes(query)]

class JPCollection:
    def __init__(self, anki_collection: Collection):
        backend_facade = BackEndFacade(anki_collection)
        self.anki_collection = anki_collection
        self.vocab = VocabCollection(backend_facade)
        self.kanji = KanjiCollection(backend_facade)
        self.sentences = SentenceCollection(backend_facade)
        self.radicals = RadicalCollection(backend_facade)

    def unsuspend_note_cards(self, note: JPNote, name: str) -> None:
        print("Unsuspending {}: {}".format(JPNote.get_note_type_name(note), name))
        self.anki_collection.sched.unsuspend_cards(note.card_ids())
