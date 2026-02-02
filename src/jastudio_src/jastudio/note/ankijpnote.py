from __future__ import annotations

from typing import TYPE_CHECKING, cast

import jaslib.note.jpnote
from anki.models import NotetypeDict
from autoslot import Slots
from jaslib.note.note_constants import NoteTypes
from jaslib.sysutils.typed import str_
from jaslib.sysutils.weak_ref import WeakRefable
from jastudio.note.jpnotedata_shim import JPNoteDataShim

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.notes import Note

class AnkiJPNote(WeakRefable, Slots):
    # def __init__(self, note: Note) -> None:
    #     self.weakref: WeakRef[JPNote] = WeakRef(self)
    #     self.recursive_flush_guard: NoteRecursiveFlushGuard = NoteRecursiveFlushGuard(self.weakref)
    #     self.backend_note: Note = note
    #     self.__hash_value: int = 0
    #
    #     string_auto_interner.auto_intern_list(note.fields)  # saves something like 20-30MB of memory on my collection
    #
    #     self.tags: NoteTags = NoteTags(self.weakref)
    #     self._id_cache: NoteId = note.id
    #
    # @property
    # def is_flushing(self) -> bool: return self.recursive_flush_guard.is_flushing
    #
    # @override
    # def __eq__(self, other: object) -> bool:
    #     ex_assert.not_none(self.get_id(), "You cannot compare or hash a note that has not been saved yet since it has no id")
    #     return isinstance(other, JPNote) and other.get_id() == self.get_id()
    #
    # @override
    # def __hash__(self) -> int:
    #     if not self.__hash_value:
    #         self.__hash_value = int(self.get_id())
    #         ex_assert.that(self.__hash_value != 0, "You cannot compare or hash a note that has not been saved yet since it has no id")
    #     return self.__hash_value
    #
    # @override
    # def __repr__(self) -> str:
    #     return f"""{self.get_question()}: {self.get_answer()}"""
    #
    # @property
    # def collection(self) -> JPCollection:
    #     return app.col()
    #
    # def get_question(self) -> str:
    #     value = self.get_field(MyNoteFields.question)
    #     return value if value else "[EMPTY]"
    #
    # def get_answer(self) -> str:
    #     return self.get_field(MyNoteFields.answer)
    #
    # def is_studying(self, card: str = "") -> bool:
    #     return noteutils.has_card_being_studied_cached(self.backend_note, card)
    #
    @classmethod
    def note_from_card(cls, card: Card) -> jaslib.note.jpnote.JPNote:
        note = card.note()
        return cls.note_from_note(note)

    @classmethod
    def note_from_note(cls, note: Note) -> jaslib.note.jpnote.JPNote:
        from jaslib.note.kanjinote import KanjiNote
        from jaslib.note.sentences.sentencenote import SentenceNote
        from jaslib.note.vocabulary.vocabnote import VocabNote

        data = JPNoteDataShim.from_note(note)

        if cls.get_note_type(note) == NoteTypes.Kanji: return KanjiNote(data)
        if cls.get_note_type(note) == NoteTypes.Vocab: return VocabNote(data)
        if cls.get_note_type(note) == NoteTypes.Sentence: return SentenceNote(data)
        return jaslib.note.jpnote.JPNote(data)

    @classmethod
    def get_note_type(cls, note: Note) -> str:
        return str_(cast(NotetypeDict, note.note_type())["name"])  # pyright: ignore[reportAny]

    # def get_type(self) -> NoteTypeEx:
    #     return NoteTypeEx.from_dict(non_optional(self.backend_note.note_type()))
    #
    # def get_direct_dependencies(self) -> QSet[JPNote]:
    #     return QSet()
    #
    # def _on_tags_updated(self) -> None:
    #     """Called when tags are modified. Subclasses can override to invalidate cached state."""
    #     pass
    #
    # def _get_dependencies_recursive(self, found: QSet[JPNote]) -> QSet[JPNote]:
    #     if self in found:
    #         return found
    #     found.add(self)
    #     for dependency in self.get_direct_dependencies():
    #         dependency._get_dependencies_recursive(found)
    #     return found
    #
    # def get_dependencies_recursive(self) -> QSet[JPNote]:
    #     return self._get_dependencies_recursive(QSet())
    #
    # def get_id(self) -> NoteId:
    #     value = self._id_cache
    #     if value: return value
    #
    #     self._id_cache = self.backend_note.id
    #     return self._id_cache
    #
    # def cards(self) -> list[CardEx]:
    #     return [CardEx(card) for card in self.backend_note.cards()]
    #
    # def has_suspended_cards(self) -> bool:
    #     return any(_card for _card in self.cards() if _card.is_suspended())
    #
    # def has_active_cards(self) -> bool:
    #     return any(_card for _card in self.cards() if not _card.is_suspended())
    #
    # def has_suspended_cards_or_depencies_suspended_cards(self) -> bool:
    #     return any(note for note in self.get_dependencies_recursive() if note.has_suspended_cards())
    #
    # def unsuspend_all_cards(self) -> None:
    #     for card in self.cards(): card.un_suspend()
    #
    # def unsuspend_all_cards_and_dependencies(self) -> None:
    #     for note in self.get_dependencies_recursive():
    #         note.unsuspend_all_cards()
    #
    # def suspend_all_cards(self) -> None:
    #     for card in self.cards(): card.suspend()
    #
    # def update_generated_data(self) -> None:
    #     noteutils.remove_from_studying_cache(self.get_id())
    #
    # def get_field(self, field_name: str) -> str:
    #     return self.backend_note[field_name]
    #
    # def _is_persisted(self) -> bool:
    #     return int(self.backend_note.id) != 0
    #
    # def _flush(self) -> None:
    #     if self._is_persisted():
    #         self.recursive_flush_guard.flush()
    #
    # def set_field(self, field_name: str, value: str) -> None:
    #     field_value = self.backend_note[field_name]
    #     if field_value != value:
    #         self.backend_note[field_name] = value
    #         self._flush()
    #
    # def priority_tag_value(self) -> int:
    #     for tag in self.tags:
    #         if tag.name.startswith(Tags.priority_folder):
    #             return int(ex_str.first_number(tag.name))
    #     return 0
    #
    # def get_meta_tags(self) -> QSet[str]:
    #     tags: QSet[str] = QSet()
    #     for tag in self.tags:
    #         if tag.name.startswith(Tags.priority_folder):
    #             if "high" in tag.name: tags.add("high_priority")
    #             if "low" in tag.name: tags.add("low_priority")
    #
    #     if self.is_studying(CardTypes.reading) or self.is_studying(CardTypes.listening): tags.add("is_studying")
    #     if self.is_studying(CardTypes.reading): tags.add("is_studying_reading")
    #     if self.is_studying(CardTypes.listening): tags.add("is_studying_listening")
    #     if self.tags.contains(Tags.TTSAudio): tags.add("tts_audio")
    #
    #     return tags
    #
    # def get_source_tag(self) -> str:
    #     source_tags = [t for t in self.tags if t.name.startswith(Tags.Source.folder)]
    #     if source_tags:
    #         source_tags = sorted(source_tags, key=lambda tag: len(tag.name))
    #         return source_tags[0].name[len(Tags.Source.folder):]
    #     return ""
