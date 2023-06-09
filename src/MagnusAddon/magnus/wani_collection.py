from typing import List

import anki

from magnus.my_anki import *
from magnus.utils import ListUtils
from magnus.wani_utils import CardUtils
from magnus.wanikani_note import *


class WaniCollection:
    def fetch_notes_by_note_type_and_field_value(note_type: str, field: str,
                                                 field_values: List) -> List[anki.notes.Note]:
        note_ids = [mw.col.find_notes(
            "{}:{} {}:{}".format(SearchTags.NoteType, note_type, field, field_value))
            for field_value in field_values]

        note_ids = ListUtils.flatten_list(note_ids)
        notes = WaniCollection.fetch_notes_by_id(note_ids)
        return notes

    def fetch_notes_by_note_type(note_type: str) -> List[anki.notes.Note]:
        note_ids = [mw.col.find_notes("{}:{}".format(SearchTags.NoteType, note_type))]
        note_ids = ListUtils.flatten_list(note_ids)
        notes = WaniCollection.fetch_notes_by_id(note_ids)
        return notes

    def fetch_kanji_notes(field_values: List) -> List[WaniKanjiNote]:
        notes = WaniCollection.fetch_notes_by_note_type_and_field_value(Wani.NoteType.Kanji, Wani.KanjiFields.Kanji,
                                                                        field_values)
        kanji_notes = [WaniKanjiNote(note) for note in notes]
        return kanji_notes

    def fetch_radical_notes(field_values: List) -> List[WaniRadicalNote]:
        notes = WaniCollection.fetch_notes_by_note_type_and_field_value(Wani.NoteType.Radical,
                                                                        Wani.RadicalFields.Radical_Name, field_values)
        radical_notes = [WaniRadicalNote(note) for note in notes]
        return radical_notes

    def fetch_vocab_notes(field_values: List) -> List[WaniVocabNote]:
        notes = WaniCollection.fetch_notes_by_note_type_and_field_value(Wani.NoteType.Vocab, Wani.KanjiFields.Kanji,
                                                                        field_values)
        vocab_notes = [WaniVocabNote(note) for note in notes]
        return vocab_notes

    def fetch_all_radical_notes() -> List[WaniRadicalNote]:
        notes = WaniCollection.fetch_notes_by_note_type(Wani.NoteType.Radical)
        radical_notes = [WaniRadicalNote(note) for note in notes]
        return radical_notes

    def fetch_all_kanji_notes() -> List[WaniKanjiNote]:
        notes = WaniCollection.fetch_notes_by_note_type(Wani.NoteType.Kanji)
        kanji_notes = [WaniKanjiNote(note) for note in notes]
        return kanji_notes

    def fetch_all_vocab_notes() -> List[WaniVocabNote]:
        notes = WaniCollection.fetch_notes_by_note_type(Wani.NoteType.Vocab)
        vocab_notes = [WaniVocabNote(note) for note in notes]
        vocab_notes = [vocab for vocab in vocab_notes if vocab.is_wani_vocab()]
        return vocab_notes

    def fetch_notes_by_id(note_ids: List) -> List[anki.notes.Note]:
        return [mw.col.get_note(note_id) for note_id in note_ids]

    def unsuspend_note_cards(note: WaniNote, name: str) -> None:
        print("Unsuspending {}: {}".format(WaniNote.get_note_type_name(note), name))
        mw.col.sched.unsuspend_cards(note.card_ids())

    def prioritize_note_cards(note: WaniNote, name: str) -> None:
        cards = [mw.col.get_card(id) for id in note.card_ids()]
        for card in cards:
            CardUtils.prioritize(card)
