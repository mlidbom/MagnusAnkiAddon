from __future__ import annotations
from anki.cards import Card
from anki.notes import Note


from wanikani.wani_constants import Wani


class MyNote:
    def __init__(self, note: Note):
        self._note = note

    @classmethod
    def note_from_card(cls, card: Card) -> MyNote:
        note = card.note()
        return cls.note_from_note(note)

    @classmethod
    def note_from_note(cls, note) -> MyNote:
        from note.sentencenote import SentenceNote
        from note.kanjinote import KanjiNote
        from note.radicalnote import RadicalNote
        from note.vocabnote import VocabNote

        if cls.get_note_type(note) == Wani.NoteType.Kanji:
            return KanjiNote(note)
        elif cls.get_note_type(note) == Wani.NoteType.Vocab:
            return VocabNote(note)
        elif cls.get_note_type(note) == Wani.NoteType.Radical:
            return RadicalNote(note)
        elif cls.get_note_type(note) == Wani.NoteType.Sentence:
            return SentenceNote(note)
        return MyNote(note)

    @staticmethod
    def get_note_type(note: Note) -> str:
        return note.note_type()["name"]

    @classmethod
    def _on_note_edited(cls, note: Note):
        cls.note_from_note(note)._on_edited()

    def _on_edited(self) -> None: pass

    def get_field(self, field_name: str) -> str: return self._note[field_name]

    def set_field(self, field_name: str, value: str) -> None:
        field_value = self._note[field_name]
        if field_value != value:
            self._note[field_name] = value
            self._note.flush()

    def has_tag(self, tag:str) -> bool: return tag in self._note.tags

    def set_tag(self, tag:str) -> None:
        if not self.has_tag(tag):
            self._note.tags.append(tag)
            self._note.flush()

    def last_edit_time(self) -> int:
        return self._note.mod