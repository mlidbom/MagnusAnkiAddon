from __future__ import annotations

from typing import TYPE_CHECKING, cast

from anki.models import NotetypeDict
from anki_extentions.card_ex import CardEx
from anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from ankiutils import app
from autoslot import Slots
from note import noteutils
from note.note_constants import CardTypes, MyNoteFields, NoteTypes, Tags
from note.note_flush_guard import NoteFlushGuard
from sysutils import ex_assert, ex_str
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.typed import non_optional, str_
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:

    from anki.cards import Card
    from anki.notes import Note, NoteId
    from note.collection.jp_collection import JPCollection

class JPNote(Slots):
    __slots__ = ["__weakref__"]
    def __init__(self, note: Note) -> None:
        self.weakref: WeakRef[JPNote] = WeakRef(self)
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self.flush_guard = NoteFlushGuard(self.weakref)
        self.backend_note = note
        self.__hash_value = 0

    @property
    def is_flushing(self) -> bool: return self.flush_guard.is_flushing

    def __eq__(self, other: object) -> bool:
        ex_assert.not_none(self.get_id(), "You cannot compare or hash a note that has not been saved yet since it has no id")
        return isinstance(other, JPNote) and other.get_id() == self.get_id()

    def __hash__(self) -> int:
        if not self.__hash_value:
            self.__hash_value = int(self.get_id())
            ex_assert.that(self.__hash_value != 0, "You cannot compare or hash a note that has not been saved yet since it has no id")
        return self.__hash_value

    def __repr__(self) -> str: return self.get_question()

    @property
    def _app(self) -> app:
        return app

    @property
    def collection(self) -> JPCollection: return self._app.col()

    def get_question(self) -> str:
        value = self.get_field(MyNoteFields.question).strip()
        return value if value else "[EMPTY]"

    def get_answer(self) -> str: return self.get_field(MyNoteFields.answer)

    def is_studying(self, card: str = "") -> bool:
        return noteutils.has_card_being_studied_cached(self.backend_note, card)

    @classmethod
    def note_from_card(cls, card: Card) -> JPNote:
        note = card.note()
        return cls.note_from_note(note)

    @classmethod
    def note_from_note(cls, note: Note) -> JPNote:
        from note.kanjinote import KanjiNote
        from note.sentences.sentencenote import SentenceNote
        from note.vocabulary.vocabnote import VocabNote

        if cls.get_note_type(note) == NoteTypes.Kanji: return KanjiNote(note)
        if cls.get_note_type(note) == NoteTypes.Vocab: return VocabNote(note)
        if cls.get_note_type(note) == NoteTypes.Sentence: return SentenceNote(note)
        return JPNote(note)

    @staticmethod
    def get_note_type(note: Note) -> str:
        return str_(cast(NotetypeDict, note.note_type())["name"])

    def get_type(self) -> NoteTypeEx: return NoteTypeEx.from_dict(non_optional(self.backend_note.note_type()))

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

    def get_id(self) -> NoteId: return self.backend_note.id
    def is_wani_note(self) -> bool: return Tags.Wani in self.backend_note.tags

    def cards(self) -> list[CardEx]: return [CardEx(card) for card in self.backend_note.cards()]
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

    def get_field(self, field_name: str) -> str: return self.backend_note[field_name]

    def _is_persisted(self) -> bool: return int(self.backend_note.id) != 0

    def _flush(self) -> None:
        if self._is_persisted():
            self.flush_guard.flush()

    def set_field(self, field_name: str, value: str) -> None:
        field_value = self.backend_note[field_name]
        if field_value != value:
            self.backend_note[field_name] = value
            self._flush()

    def get_tags(self) -> list[str]: return self.backend_note.tags

    def has_tag(self, tag: str) -> bool: return self.backend_note.has_tag(tag)

    def priority_tag_value(self) -> int:
        for tag in self.backend_note.tags:
            if tag.startswith(Tags.priority_folder):
                return int(ex_str.first_number(tag))
        return 0

    def get_meta_tags(self) -> set[str]:
        tags: set[str] = set()
        for tag in self.backend_note.tags:
            if tag.startswith(Tags.priority_folder):
                if "high" in tag: tags.add("high_priority")
                if "low" in tag: tags.add("low_priority")

        if self.is_studying(CardTypes.reading) or self.is_studying(CardTypes.listening): tags.add("is_studying")
        if self.is_studying(CardTypes.reading): tags.add("is_studying_reading")
        if self.is_studying(CardTypes.listening): tags.add("is_studying_listening")
        if self.has_tag(Tags.TTSAudio): tags.add("tts_audio")

        return tags

    def get_source_tag(self) -> str:
        source_tags = [t for t in self.get_tags() if t.startswith(Tags.source_folder)]
        if source_tags:
            source_tags = sorted(source_tags, key=lambda tag: len(tag))
            return source_tags[0][len(Tags.source_folder):]
        return ""

    def remove_tag(self, tag: str) -> None:
        if self.has_tag(tag):
            self.backend_note.remove_tag(tag)
            self._flush()

    def set_tag(self, tag: str) -> None:
        if not self.has_tag(tag):
            self.backend_note.tags.append(tag)
            self._flush()

    def toggle_tag(self, tag: str, on: bool) -> None:
        if on:
            self.set_tag(tag)
        else:
            self.remove_tag(tag)
