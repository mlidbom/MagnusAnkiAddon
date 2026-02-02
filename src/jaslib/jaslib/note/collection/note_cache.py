from __future__ import annotations

from typing import override

from autoslot import Slots
from jaslib.note.jpnote import JPNote, NoteId
from jaslib.sysutils.collections.default_dict_case_insensitive import DefaultDictCaseInsensitive
from typed_linq_collections.collections.q_list import QList
from typed_linq_collections.collections.q_set import QSet


class CachedNote(Slots):
    def __init__(self, note: JPNote) -> None:
        self.id: NoteId = note.get_id()
        self.question: str = note.get_question()

class NoteCacheBase[TNote: JPNote](Slots):
    def __init__(self, cached_note_type: type[TNote]) -> None:
        self._note_type: type[TNote] = cached_note_type
        self._by_id: dict[NoteId, TNote] = {}

    def with_id_or_none(self, note_id: NoteId) -> TNote | None:
        return self._by_id.get(note_id, None)

    def refresh_in_cache(self, note: TNote) -> None: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def remove_from_cache(self, note: TNote) -> None: raise NotImplementedError() # pyright: ignore[reportUnusedParameter]
    def add_to_cache(self, note: TNote) -> None: raise NotImplementedError() # pyright: ignore[reportUnusedParameter]

class NoteCache[TNote: JPNote, TSnapshot: CachedNote](NoteCacheBase[TNote], Slots):
    def __init__(self, cached_note_type: type[TNote]) -> None:
        super().__init__(cached_note_type)
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets
        self._by_question: DefaultDictCaseInsensitive[QList[TNote]] = DefaultDictCaseInsensitive(QList[TNote])
        self._snapshot_by_id: dict[NoteId, TSnapshot] = {}

        self._deleted: QSet[NoteId] = QSet()

        self._flushing: bool = False

    def all(self) -> QList[TNote]:
        return QList(self._by_id.values())

    def with_question(self, question: str) -> QList[TNote]:
        return self._by_question.get_value_or_default(question).to_list()

    def _create_snapshot(self, note: TNote) -> TSnapshot: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def _inheritor_remove_from_cache(self, note: TNote, snapshot: TSnapshot) -> None: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def _inheritor_add_to_cache(self, note: TNote, snapshot: TSnapshot) -> None: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]

    @override
    def refresh_in_cache(self, note: TNote) -> None:
        self.remove_from_cache(note)
        self.add_to_cache(note)

    @override
    def remove_from_cache(self, note: TNote) -> None:
        assert note.get_id()
        cached = self._snapshot_by_id.pop(note.get_id())
        self._by_id.pop(note.get_id())
        self._by_question[cached.question].remove(note)
        self._inheritor_remove_from_cache(note, cached)

    _next_note_id: NoteId = 1
    @override
    def add_to_cache(self, note: TNote) -> None:
        if note.get_id() in self._by_id: return
        if note.get_id() == 0:
            note.set_id(self._next_note_id)
            NoteCache._next_note_id += 1

        self._by_id[note.get_id()] = note
        snapshot = self._create_snapshot(note)
        self._snapshot_by_id[note.get_id()] = snapshot
        self._by_question[note.get_question()].append(note)
        self._inheritor_add_to_cache(note, snapshot)
