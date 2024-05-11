from __future__ import annotations

from abc import ABC
from typing import Any, cast, Sequence

from anki.cards import Card, CardId
from anki.models import NotetypeDict
from anki.notes import Note, NoteId

from note import noteutils
from note.note_constants import Mine, MyNoteFields, NoteTypes
from sysutils.typed import checked_cast

class JPNote(ABC):
    def __init__(self, note: Note):
        self._note = note
        self._is_flushing: bool = False

    def __eq__(self, other: Any) -> bool:
        assert self.get_id(), "You cannot compare or hash a note that has not been saved yet since it has no id"
        return isinstance(other, JPNote) and other.get_id() == self.get_id()

    def __hash__(self) -> int:
        assert self.get_id(), "You cannot compare or hash a note that has not been saved yet since it has no id"
        return hash(self.get_id())

    def __repr__(self) -> str:
        return f"""{self.get_question()} : {self.get_answer()}"""

    def get_question(self) -> str: return self.get_field(MyNoteFields.question)
    def get_answer(self) -> str: return self.get_field(MyNoteFields.answer)

    def is_studying_cached(self) -> bool:
        return noteutils.has_card_being_studied_cached(self._note)

    @classmethod
    def note_from_card(cls, card: Card) -> JPNote:
        note = card.note()
        return cls.note_from_note(note)

    @classmethod
    def note_from_note(cls, note: Note) -> JPNote:
        from note.sentencenote import SentenceNote
        from note.kanjinote import KanjiNote
        from note.radicalnote import RadicalNote
        from note.vocabnote import VocabNote

        if cls.get_note_type(note) == NoteTypes.Kanji: return KanjiNote(note)
        elif cls.get_note_type(note) == NoteTypes.Vocab: return VocabNote(note)
        elif cls.get_note_type(note) == NoteTypes.Radical: return RadicalNote(note)
        elif cls.get_note_type(note) == NoteTypes.Sentence: return SentenceNote(note)
        return JPNote(note)

    @staticmethod
    def get_note_type(note: Note) -> str:
        return checked_cast(str, cast(NotetypeDict, note.note_type())["name"])

    def get_note_type_name(self) -> str: return self.get_note_type(self._note)

    def delete(self) -> None:
        from ankiutils import app
        app.anki_collection().remove_notes([self._note.id])

    def get_id(self) -> NoteId: return self._note.id
    def card_ids(self) -> Sequence[CardId]: return self._note.card_ids()
    def is_wani_note(self) -> bool: return Mine.Tags.Wani in self._note.tags

    def update_generated_data(self) -> None:
        pass

    def _on_before_flush(self) -> None:
        self._is_flushing = True
        try:
            self.update_generated_data()
        finally:
            self._is_flushing = False

    def get_field(self, field_name: str) -> str: return self._note[field_name]

    def _is_persisted(self) -> bool: return int(self._note.id) != 0

    def _flush(self) -> None:
        if self._is_persisted():
            if not self._is_flushing: # We need to cancel infinite recursion here somehow...
                self._is_flushing = True
                try:
                    self._note.flush()
                finally:
                    self._is_flushing = False

    def set_field(self, field_name: str, value: str) -> None:
        field_value = self._note[field_name]
        if field_value != value:
            self._note[field_name] = value
            self._flush()

    def get_tags(self) -> list[str]: return self._note.tags

    def has_tag(self, tag: str) -> bool: return tag in self._note.tags

    def set_tag(self, tag: str) -> None:
        if not self.has_tag(tag):
            self._note.tags.append(tag)
            self._flush()

    def last_edit_time(self) -> int:
        return self._note.mod
