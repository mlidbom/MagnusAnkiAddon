from __future__ import annotations

from typing import TYPE_CHECKING

from anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from sysutils import rassert

if TYPE_CHECKING:
    from anki.cards import Card, CardId
    from anki.notes import Note, NoteId
    from note.collection.jp_collection import JPCollection

from abc import ABC
from typing import Any, Sequence, cast

from anki.models import NotetypeDict
from anki_extentions.card_ex import CardEx
from note import noteutils
from note.note_constants import CardTypes, Mine, MyNoteFields, NoteTypes
from sysutils import ex_str
from sysutils.typed import non_optional, str_


class JPNote(ABC):
    def __init__(self, note: Note):
        self._note = note
        self._is_updating_generated_data: bool = False
        self._generated_data_was_updated = False
        self.__hash_value = 0

    def __eq__(self, other: Any) -> bool:
        rassert.not_none(self.get_id(), "You cannot compare or hash a note that has not been saved yet since it has no id")
        return isinstance(other, JPNote) and other.get_id() == self.get_id()


    def __hash__(self) -> int:
        if not self.__hash_value:
            assert self.get_id(), "You cannot compare or hash a note that has not been saved yet since it has no id"
            self.__hash_value = hash(self.get_id())
        return self.__hash_value

    def __repr__(self) -> str:
        return f"""{self.get_question()} : {self.get_answer()}"""

    @property
    def collection(self) -> JPCollection:
        from ankiutils import app
        return app.col()

    def get_question(self) -> str:
        value = self.get_field(MyNoteFields.question).strip()
        return value if value else "[EMPTY]"

    def get_answer(self) -> str: return self.get_field(MyNoteFields.answer)

    def is_studying(self, card:str = "") -> bool:
        return noteutils.has_card_being_studied_cached(self._note, card)

    @classmethod
    def note_from_card(cls, card: Card) -> JPNote:
        note = card.note()
        return cls.note_from_note(note)

    @classmethod
    def note_from_note(cls, note: Note) -> JPNote:
        from note.kanjinote import KanjiNote
        from note.radicalnote import RadicalNote
        from note.sentencenote import SentenceNote
        from note.vocabnote import VocabNote

        if cls.get_note_type(note) == NoteTypes.Kanji: return KanjiNote(note)
        elif cls.get_note_type(note) == NoteTypes.Vocab: return VocabNote(note)
        elif cls.get_note_type(note) == NoteTypes.Radical: return RadicalNote(note)
        elif cls.get_note_type(note) == NoteTypes.Sentence: return SentenceNote(note)
        return JPNote(note)

    @staticmethod
    def get_note_type(note: Note) -> str:
        return str_(cast(NotetypeDict, note.note_type())["name"])

    def get_type(self) -> NoteTypeEx: return NoteTypeEx.from_dict(non_optional(self._note.note_type()))

    def get_note_type_name(self) -> str: return self.get_note_type(self._note)

    def get_direct_dependencies(self) -> set[JPNote]:
        return set()

    def _get_dependencies_recursive(self, found: set[JPNote]) -> set[JPNote]:
        if self in found:
            return found
        found.add(self)
        for dependency in self.get_direct_dependencies():
            dependency._get_dependencies_recursive(found)
        return found

    def get_dependencies_recursive(self) -> set[JPNote]:
        return self._get_dependencies_recursive(set())

    def get_id(self) -> NoteId: return self._note.id
    def card_ids(self) -> Sequence[CardId]: return self._note.card_ids()
    def is_wani_note(self) -> bool: return Mine.Tags.Wani in self._note.tags

    def cards(self) -> list[CardEx]: return [CardEx(card) for card in self._note.cards()]
    def has_suspended_cards(self) -> bool: return any(_card for _card in self.cards() if _card.is_suspended())
    def has_active_cards(self) -> bool: return any(_card for _card in self.cards() if not _card.is_suspended())

    def has_suspended_cards_or_depencies_suspended_cards(self) -> bool: return any(note for note in self.get_dependencies_recursive() if note.has_suspended_cards())


    def unsuspend_all_cards(self) -> None:
        for card in self.cards(): card.un_suspend()

    def unsuspend_all_cards_and_dependencies(self) -> None:
        for note in self.get_dependencies_recursive():
            note.unsuspend_all_cards()

    def suspend_all_cards(self) -> None:
        for card in self.cards(): card.suspend()

    def update_generated_data(self) -> None:
        noteutils.remove_from_studying_cache(self.get_id())

    def get_field(self, field_name: str) -> str: return self._note[field_name]

    def _is_persisted(self) -> bool: return int(self._note.id) != 0

    def _flush(self) -> None:
        if self._is_persisted():
            if self._is_updating_generated_data: # We need to cancel infinite recursion here somehow...
                self._generated_data_was_updated = True
                return

            self._is_updating_generated_data = True
            try:
                self._note.col.update_note(self._note)
            finally:
                self._is_updating_generated_data = False

    def set_field(self, field_name: str, value: str) -> None:
        field_value = self._note[field_name]
        if field_value != value:
            self._note[field_name] = value
            self._flush()

    def get_tags(self) -> list[str]: return self._note.tags

    def has_tag(self, tag: str) -> bool: return self._note.has_tag(tag)

    def priority_tag_value(self) -> int:
        for tag in self._note.tags:
            if tag.startswith(Mine.Tags.priority_folder):
                return int(ex_str.first_number(tag))
        return 0

    def get_meta_tags(self) -> set[str]:
        tags:set[str] = set()
        for tag in self._note.tags:
            if tag.startswith(Mine.Tags.priority_folder):
                if "high" in tag: tags.add("high_priority")
                if "low" in tag: tags.add("low_priority")

        if self.is_studying(CardTypes.reading) or self.is_studying(CardTypes.listening): tags.add("is_studying")
        if self.is_studying(CardTypes.reading): tags.add("is_studying_reading")
        if self.is_studying(CardTypes.listening): tags.add("is_studying_listening")
        if self.has_tag(Mine.Tags.TTSAudio): tags.add("tts_audio")

        return tags

    def get_source_tag(self) -> str:
        source_tags = [t for t in self.get_tags() if t.startswith(Mine.Tags.source_folder)]
        if source_tags:
            source_tags = sorted(source_tags, key=lambda tag: len(tag))
            return source_tags[0][len(Mine.Tags.source_folder):]
        return ""


    def remove_tag(self, tag: str) -> None:
        if self.has_tag(tag):
            self._note.remove_tag(tag)
            self._flush()

    def set_tag(self, tag: str) -> None:
        if not self.has_tag(tag):
            self._note.tags.append(tag)
            self._flush()

    def toggle_tag(self, tag:str, on:bool) -> None:
        if on:
            self.set_tag(tag)
        else:
            self.remove_tag(tag)
