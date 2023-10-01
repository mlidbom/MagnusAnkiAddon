from typing import List, Sequence

import anki
from anki.notes import NoteId, Note

from ankiutils.anki_shim import facade
from ankiutils.search_utils import Builtin
from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.radicalnote import RadicalNote
from note.vocabnote import VocabNote
from note.cardutils import CardUtils
from note.kanjinote import KanjiNote
from note.note_constants import NoteFields, NoteTypes
from sysutils.listutils import ListUtils


class JPLegacyCollection:
    @staticmethod
    def list_sentence_notes() -> list[SentenceNote]:
        return [SentenceNote(note) for note in JPLegacyCollection.fetch_notes_by_note_type(NoteTypes.Sentence)]

    @staticmethod
    def fetch_notes_by_note_type_and_field_value(note_type: str, field: str,
                                                 field_values: List) -> List[anki.notes.Note]:
        note_ids = [facade.anki_collection().find_notes(
            f"{Builtin.Note}:{note_type} {field}:{field_value}")
            for field_value in field_values]

        note_ids = ListUtils.flatten_list(note_ids)
        notes = JPLegacyCollection.fetch_notes_by_id(note_ids)
        return notes

    @staticmethod
    def fetch_notes_by_note_type(note_type: str) -> List[anki.notes.Note]:
        notes = JPLegacyCollection._search_notes("{}:{}".format(Builtin.Note, note_type))
        return notes

    @classmethod
    def search_vocab_notes(cls, query: str) -> list[VocabNote]:
        return [VocabNote(note) for note in (cls._search_notes(query))]

    @classmethod
    def search_kanji_notes(cls, query: str) -> list[KanjiNote]:
        return [KanjiNote(note) for note in cls._search_notes(query)]

    @staticmethod
    def _search_notes(query: str) -> list[Note]:
        note_ids = [facade.anki_collection().find_notes(query)]
        note_ids = ListUtils.flatten_list(note_ids)
        notes = JPLegacyCollection.fetch_notes_by_id(note_ids)
        return notes

    @staticmethod
    def fetch_kanji_notes(field_values: List) -> List[KanjiNote]:
        notes = JPLegacyCollection.fetch_notes_by_note_type_and_field_value(NoteTypes.Kanji, NoteFields.Kanji.question,
                                                                            field_values)
        kanji_notes = [KanjiNote(note) for note in notes]
        return kanji_notes

    @staticmethod
    def fetch_radical_notes(field_values: List) -> List[RadicalNote]:
        notes = JPLegacyCollection.fetch_notes_by_note_type_and_field_value(NoteTypes.Radical,
                                                                            NoteFields.Radical.answer, field_values)
        radical_notes = [RadicalNote(note) for note in notes]
        return radical_notes

    @staticmethod
    def fetch_vocab_notes(field_values: List) -> List[VocabNote]:
        notes = JPLegacyCollection.fetch_notes_by_note_type_and_field_value(NoteTypes.Vocab, NoteFields.Kanji.question,
                                                                            field_values)
        vocab_notes = [VocabNote(note) for note in notes]
        return vocab_notes

    @staticmethod
    def fetch_all_radical_notes() -> List[RadicalNote]:
        notes = JPLegacyCollection.fetch_notes_by_note_type(NoteTypes.Radical)
        radical_notes = [RadicalNote(note) for note in notes]
        return radical_notes

    @staticmethod
    def fetch_all_kanji_notes() -> List[KanjiNote]:
        notes = JPLegacyCollection.fetch_notes_by_note_type(NoteTypes.Kanji)
        kanji_notes = [KanjiNote(note) for note in notes]
        return kanji_notes

    @staticmethod
    def fetch_all_wani_kanji_notes() -> list[KanjiNote]:
        return [kanji for kanji in JPLegacyCollection.fetch_all_kanji_notes() if kanji.is_wani_note()]

    @staticmethod
    def fetch_all_wani_vocab_notes() -> List[VocabNote]:
        notes = JPLegacyCollection.fetch_notes_by_note_type(NoteTypes.Vocab)
        vocab_notes = [VocabNote(note) for note in notes]
        vocab_notes = [vocab for vocab in vocab_notes if vocab.is_wani_note()]
        return vocab_notes

    @staticmethod
    def fetch_all_vocab_notes() -> List[VocabNote]:
        notes = JPLegacyCollection.fetch_notes_by_note_type(NoteTypes.Vocab)
        vocab_notes = [VocabNote(note) for note in notes]
        return vocab_notes

    @staticmethod
    def fetch_notes_by_id(note_ids: Sequence[NoteId]) -> List[anki.notes.Note]:
        return [facade.anki_collection().get_note(note_id) for note_id in note_ids]

    @staticmethod
    def unsuspend_note_cards(note: JPNote, name: str) -> None:
        print("Unsuspending {}: {}".format(JPNote.get_note_type_name(note), name))
        facade.anki_collection().sched.unsuspend_cards(note.card_ids())

    @staticmethod
    def prioritize_note_cards(note: JPNote) -> None:
        cards = [facade.anki_collection().get_card(card_id) for card_id in note.card_ids()]
        for card in cards:
            CardUtils.prioritize(card)
