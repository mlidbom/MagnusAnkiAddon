from typing import List, Sequence

import anki
from anki.notes import NoteId, Note

from ankiutils.anki_shim import facade
from ankiutils.search_utils import Builtin
from note.sentencenote import SentenceNote
from sysutils.utils import ListUtils
from note.waninote import WaniNote
from note.waniradicalnote import WaniRadicalNote
from note.wanivocabnote import WaniVocabNote
from wanikani.utils.wani_utils import CardUtils
from note.wanikanjinote import WaniKanjiNote
from wanikani.wani_constants import Wani


class WaniCollection:
    @staticmethod
    def list_sentence_notes() -> list[SentenceNote]:
        return [SentenceNote(note) for note in WaniCollection.fetch_notes_by_note_type(Wani.NoteType.Sentence)]

    @staticmethod
    def fetch_notes_by_note_type_and_field_value(note_type: str, field: str,
                                                 field_values: List) -> List[anki.notes.Note]:
        note_ids = [facade.col().find_notes(
            f"{Builtin.Note}:{note_type} {field}:{field_value}")
            for field_value in field_values]

        note_ids = ListUtils.flatten_list(note_ids)
        notes = WaniCollection.fetch_notes_by_id(note_ids)
        return notes

    @staticmethod
    def fetch_notes_by_note_type(note_type: str) -> List[anki.notes.Note]:
        notes = WaniCollection._search_notes("{}:{}".format(Builtin.Note, note_type))
        return notes

    @classmethod
    def search_vocab_notes(cls, query: str) -> list[WaniVocabNote]:
        return [WaniVocabNote(note) for note in (cls._search_notes(query))]

    @classmethod
    def search_kanji_notes(cls, query: str) -> list[WaniKanjiNote]:
        return [WaniKanjiNote(note) for note in cls._search_notes(query)]

    @staticmethod
    def _search_notes(query: str) -> list[Note]:
        note_ids = [facade.col().find_notes(query)]
        note_ids = ListUtils.flatten_list(note_ids)
        notes = WaniCollection.fetch_notes_by_id(note_ids)
        return notes

    @staticmethod
    def fetch_kanji_notes(field_values: List) -> List[WaniKanjiNote]:
        notes = WaniCollection.fetch_notes_by_note_type_and_field_value(Wani.NoteType.Kanji, Wani.KanjiFields.question,
                                                                        field_values)
        kanji_notes = [WaniKanjiNote(note) for note in notes]
        return kanji_notes

    @staticmethod
    def fetch_radical_notes(field_values: List) -> List[WaniRadicalNote]:
        notes = WaniCollection.fetch_notes_by_note_type_and_field_value(Wani.NoteType.Radical,
                                                                        Wani.RadicalFields.answer, field_values)
        radical_notes = [WaniRadicalNote(note) for note in notes]
        return radical_notes

    @staticmethod
    def fetch_vocab_notes(field_values: List) -> List[WaniVocabNote]:
        notes = WaniCollection.fetch_notes_by_note_type_and_field_value(Wani.NoteType.Vocab, Wani.KanjiFields.question,
                                                                        field_values)
        vocab_notes = [WaniVocabNote(note) for note in notes]
        return vocab_notes

    @staticmethod
    def fetch_all_radical_notes() -> List[WaniRadicalNote]:
        notes = WaniCollection.fetch_notes_by_note_type(Wani.NoteType.Radical)
        radical_notes = [WaniRadicalNote(note) for note in notes]
        return radical_notes

    @staticmethod
    def fetch_all_kanji_notes() -> List[WaniKanjiNote]:
        notes = WaniCollection.fetch_notes_by_note_type(Wani.NoteType.Kanji)
        kanji_notes = [WaniKanjiNote(note) for note in notes]
        return kanji_notes

    @staticmethod
    def fetch_all_wani_kanji_notes() -> list[WaniKanjiNote]:
        return [kanji for kanji in WaniCollection.fetch_all_kanji_notes() if kanji.is_wani_note()]

    @staticmethod
    def fetch_all_wani_vocab_notes() -> List[WaniVocabNote]:
        notes = WaniCollection.fetch_notes_by_note_type(Wani.NoteType.Vocab)
        vocab_notes = [WaniVocabNote(note) for note in notes]
        vocab_notes = [vocab for vocab in vocab_notes if vocab.is_wani_note()]
        return vocab_notes

    @staticmethod
    def fetch_all_vocab_notes() -> List[WaniVocabNote]:
        notes = WaniCollection.fetch_notes_by_note_type(Wani.NoteType.Vocab)
        vocab_notes = [WaniVocabNote(note) for note in notes]
        return vocab_notes

    @staticmethod
    def fetch_notes_by_id(note_ids: Sequence[NoteId]) -> List[anki.notes.Note]:
        return [facade.col().get_note(note_id) for note_id in note_ids]

    @staticmethod
    def unsuspend_note_cards(note: WaniNote, name: str) -> None:
        print("Unsuspending {}: {}".format(WaniNote.get_note_type_name(note), name))
        facade.col().sched.unsuspend_cards(note.card_ids())

    @staticmethod
    def prioritize_note_cards(note: WaniNote) -> None:
        cards = [facade.col().get_card(card_id) for card_id in note.card_ids()]
        for card in cards:
            CardUtils.prioritize(card)
