from typing import List, Sequence

import anki
from anki.collection import Collection

from ankiutils.search_utils import Builtin
from anki.notes import NoteId, Note
from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.radicalnote import RadicalNote
from note.vocabnote import VocabNote
from note.cardutils import CardUtils
from note.kanjinote import KanjiNote
from note.note_constants import NoteFields, NoteTypes
from sysutils import listutils


class JPCollection:
    def __init__(self, anki_collection: Collection):
        self.anki_collection = anki_collection

    def list_sentence_notes(self) -> list[SentenceNote]:
        return [SentenceNote(note) for note in self.fetch_notes_by_note_type(NoteTypes.Sentence)]


    def fetch_notes_by_note_type_and_field_value(self, note_type: str, field: str,
                                                 field_values: list[str]) -> List[anki.notes.Note]:
        note_ids = [self.anki_collection.find_notes(
            f"{Builtin.Note}:{note_type} {field}:{field_value}")
            for field_value in field_values]

        note_ids_flat = listutils.flatten(note_ids)
        notes = self.fetch_notes_by_id(note_ids_flat)
        return notes


    def fetch_notes_by_note_type(self, note_type: str) -> List[anki.notes.Note]:
        notes = self._search_notes("{}:{}".format(Builtin.Note, note_type))
        return notes


    def search_vocab_notes(self, query: str) -> list[VocabNote]:
        return [VocabNote(note) for note in (self._search_notes(query))]


    def search_kanji_notes(self, query: str) -> list[KanjiNote]:
        return [KanjiNote(note) for note in self._search_notes(query)]


    def search_sentence_notes(self, query: str) -> list[SentenceNote]:
        return [SentenceNote(note) for note in self._search_notes(query)]


    def _search_notes(self, query: str) -> list[Note]:
        note_ids = [self.anki_collection.find_notes(query)]
        note_ids_flat = listutils.flatten(note_ids)
        notes = self.fetch_notes_by_id(note_ids_flat)
        return notes


    def fetch_kanji_notes(self, field_values: list[str]) -> List[KanjiNote]:
        notes = self.fetch_notes_by_note_type_and_field_value(NoteTypes.Kanji, NoteFields.Kanji.question, field_values)
        kanji_notes = [KanjiNote(note) for note in notes]
        return kanji_notes


    def fetch_radical_notes(self, field_values: list[str]) -> List[RadicalNote]:
        notes = self.fetch_notes_by_note_type_and_field_value(NoteTypes.Radical, NoteFields.Radical.answer, field_values)
        radical_notes = [RadicalNote(note) for note in notes]
        return radical_notes


    def fetch_vocab_notes(self, field_values: list[str]) -> List[VocabNote]:
        notes = self.fetch_notes_by_note_type_and_field_value(NoteTypes.Vocab, NoteFields.Kanji.question, field_values)
        vocab_notes = [VocabNote(note) for note in notes]
        return vocab_notes


    def fetch_all_radical_notes(self) -> List[RadicalNote]:
        notes = self.fetch_notes_by_note_type(NoteTypes.Radical)
        radical_notes = [RadicalNote(note) for note in notes]
        return radical_notes


    def fetch_all_kanji_notes(self) -> List[KanjiNote]:
        notes = self.fetch_notes_by_note_type(NoteTypes.Kanji)
        kanji_notes = [KanjiNote(note) for note in notes]
        return kanji_notes


    def fetch_all_wani_kanji_notes(self) -> list[KanjiNote]:
        return [kanji for kanji in self.fetch_all_kanji_notes() if kanji.is_wani_note()]


    def fetch_all_wani_vocab_notes(self) -> List[VocabNote]:
        notes = self.fetch_notes_by_note_type(NoteTypes.Vocab)
        vocab_notes = [VocabNote(note) for note in notes]
        vocab_notes = [vocab for vocab in vocab_notes if vocab.is_wani_note()]
        return vocab_notes


    def fetch_all_vocab_notes(self) -> List[VocabNote]:
        notes = self.fetch_notes_by_note_type(NoteTypes.Vocab)
        vocab_notes = [VocabNote(note) for note in notes]
        return vocab_notes


    def fetch_notes_by_id(self, note_ids: Sequence[NoteId]) -> List[anki.notes.Note]:
        return [self.anki_collection.get_note(note_id) for note_id in note_ids]


    def unsuspend_note_cards(self, note: JPNote, name: str) -> None:
        print("Unsuspending {}: {}".format(JPNote.get_note_type_name(note), name))
        self.anki_collection.sched.unsuspend_cards(note.card_ids())


    def prioritize_note_cards(self, note: JPNote) -> None:
        cards = [self.anki_collection.get_card(card_id) for card_id in note.card_ids()]
        for card in cards:
            CardUtils.prioritize(card)
