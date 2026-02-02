from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, override

from autoslot import Slots
from jaslib.note.jpnote_data import JPNoteData
from jaslib.note.note_constants import MyNoteFields
from jaslib.note.note_flush_guard import NoteRecursiveFlushGuard
from jaslib.note.note_tags import NoteTags
from jaslib.note.tags import Tags
from jaslib.sysutils import ex_assert, ex_str
from jaslib.sysutils.weak_ref import WeakRef, WeakRefable
from typed_linq_collections.collections.q_set import QSet

from jaslib import app

if TYPE_CHECKING:
    from jaslib.note.collection.jp_collection import JPCollection

type JPNoteId = int

class JPNote(WeakRefable, Slots):
    def __init__(self, data: JPNoteData | None = None) -> None:
        self.weakref: WeakRef[JPNote] = WeakRef(self)
        self.recursive_flush_guard: NoteRecursiveFlushGuard = NoteRecursiveFlushGuard(self.weakref)
        self.__hash_value: int = 0

        self.tags: NoteTags = NoteTags(self.weakref, data)

        self._fields: dict[str, str] = data.fields if data else defaultdict(str)
        self._id_cache: JPNoteId = data.id if data else 0

    # noinspection PyUnusedFunction
    @property
    def is_flushing(self) -> bool: return self.recursive_flush_guard.is_flushing

    def get_data(self) -> JPNoteData: return JPNoteData(self.get_id(), self._fields, self.tags.to_interned_string_list())

    @override
    def __eq__(self, other: object) -> bool:
        ex_assert.not_none(self.get_id(), "You cannot compare or hash a note that has not been saved yet since it has no id")
        return isinstance(other, JPNote) and other.get_id() == self.get_id()

    def _update_in_cache(self) -> None: raise NotImplementedError()

    def is_studying(self, card_type: str | None = None) -> bool: raise NotImplementedError()  # pyright: ignore
    def is_studying_read(self) -> bool: raise NotImplementedError()
    def is_studying_listening(self) -> bool: raise NotImplementedError()


    @override
    def __hash__(self) -> int:
        if not self.__hash_value:
            self.__hash_value = int(self.get_id())
            ex_assert.that(self.__hash_value != 0, "You cannot compare or hash a note that has not been saved yet since it has no id")
        return self.__hash_value

    @override
    def __repr__(self) -> str:
        return f"""{self.get_question()}: {self.get_answer()}"""

    @property
    def collection(self) -> JPCollection:
        return app.col()

    def get_question(self) -> str:
        value = self.get_field(MyNoteFields.question)
        return value if value else "[EMPTY]"

    def get_answer(self) -> str:
        return self.get_field(MyNoteFields.answer)


    def get_direct_dependencies(self) -> QSet[JPNote]:
        return QSet()

    def _on_tags_updated(self) -> None:
        """Called when tags are modified. Subclasses can override to invalidate cached state."""
        pass

    def _get_dependencies_recursive(self, found: QSet[JPNote]) -> QSet[JPNote]:
        if self in found:
            return found
        found.add(self)
        for dependency in self.get_direct_dependencies():
            dependency._get_dependencies_recursive(found)
        return found

    # noinspection PyUnusedFunction
    def get_dependencies_recursive(self) -> QSet[JPNote]:
        return self._get_dependencies_recursive(QSet())

    def get_id(self) -> JPNoteId:
        return self._id_cache

    def set_id(self, id: JPNoteId) -> None:
        if self._id_cache != 0: raise RuntimeError("Cannot change id of a note that has already been saved")
        self._id_cache = id


    def update_generated_data(self) -> None:
        pass

    def get_field(self, field_name: str) -> str:
        return self._fields[field_name]

    def _is_persisted(self) -> bool:
        return self._id_cache != 0
        #raise NotImplementedError()
        #return int(self.backend_note.id) != 0

    def _flush(self) -> None:
        if self._is_persisted():
            self.recursive_flush_guard.flush()

    def set_field(self, field_name: str, value: str) -> None:
        field_value = self._fields[field_name]
        if field_value != value:
            self._fields[field_name] = value
            self._flush()

    # noinspection PyUnusedFunction
    def priority_tag_value(self) -> int:
        for tag in self.tags:
            if tag.name.startswith(Tags.priority_folder):
                return int(ex_str.first_number(tag.name))
        return 0

    def get_meta_tags(self) -> QSet[str]:
        tags: QSet[str] = QSet()
        for tag in self.tags:
            if tag.name.startswith(Tags.priority_folder):
                if "high" in tag.name: tags.add("high_priority")
                if "low" in tag.name: tags.add("low_priority")

        if self.tags.contains(Tags.TTSAudio): tags.add("tts_audio")

        return tags

    # noinspection PyUnusedFunction
    def get_source_tag(self) -> str:
        source_tags = [t for t in self.tags if t.name.startswith(Tags.Source.folder)]
        if source_tags:
            source_tags = sorted(source_tags, key=lambda tag: len(tag.name))
            return source_tags[0].name[len(Tags.Source.folder):]
        return ""
