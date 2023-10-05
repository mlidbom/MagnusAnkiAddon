from __future__ import annotations
from typing import Any, Sequence, cast
from anki.cards import Card, CardId
from anki.models import NotetypeDict
from anki.notes import Note, NoteId

from ankiutils import app
from note.note_constants import Mine, NoteTypes

from sysutils.typed import checked_cast


class JPNote:
    def __init__(self, note: Note):
        self._note = note

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, JPNote) and other.get_id() == self.get_id()

    def __hash__(self) -> int: return hash(self.get_id())

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

        if cls.get_note_type(note) == NoteTypes.Kanji:
            return KanjiNote(note)
        elif cls.get_note_type(note) == NoteTypes.Vocab:
            return VocabNote(note)
        elif cls.get_note_type(note) == NoteTypes.Radical:
            return RadicalNote(note)
        elif cls.get_note_type(note) == NoteTypes.Sentence:
            return SentenceNote(note)
        return JPNote(note)

    @staticmethod
    def get_note_type(note: Note) -> str:
        return checked_cast(str, cast(NotetypeDict, note.note_type())["name"])

    def get_note_type_name(self) -> str:
        # noinspection PyProtectedMember
        return checked_cast(str, self._note._note_type['name'])  # Todo: find how to do this without digging into protected members

    def delete(self) -> None:
        app.anki_collection().remove_notes([self._note.id])

    def get_id(self) -> NoteId: return self._note.id

    def card_ids(self) -> Sequence[CardId]:
        return self._note.card_ids()

    def is_wani_note(self) -> bool:
        return Mine.Tags.Wani in self._note.tags

    @classmethod
    def _on_note_edited(cls, note: Note) -> None:
        cls.note_from_note(note)._on_edited()

    def _on_edited(self) -> None: pass

    def get_field(self, field_name: str) -> str: return self._note[field_name]

    def _is_persisted(self) -> bool: return int(self._note.id) != 0

    def _flush(self) -> None:
        if self._is_persisted():
            self._note.flush()

    def set_field(self, field_name: str, value: str) -> None:
        field_value = self._note[field_name]
        if field_value != value:
            self._note[field_name] = value
            self._flush()

    def has_tag(self, tag:str) -> bool: return tag in self._note.tags

    def set_tag(self, tag:str) -> None:
        if not self.has_tag(tag):
            self._note.tags.append(tag)
            self._flush()

    def last_edit_time(self) -> int:
        return self._note.mod