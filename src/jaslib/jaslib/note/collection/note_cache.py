from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from jaslib.note.jpnote import JPNote, JPNoteId
from jaslib.sysutils.abstract_method_called_error import AbstractMethodCalledError
from jaslib.sysutils.collections.default_dict_case_insensitive import DefaultDictCaseInsensitive
from jaslib.task_runners.task_progress_runner import TaskRunner
from typed_linq_collections.collections.q_list import QList
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from collections.abc import Callable

    from jaslib.note.collection.card_studying_status import CardStudyingStatus
    from jaslib.note.jpnote_data import JPNoteData

class CachedNote(Slots):
    def __init__(self, note: JPNote) -> None:
        self.id: JPNoteId = note.get_id()
        self.question: str = note.get_question()

class NoteCacheBase[TNote: JPNote](Slots):
    def __init__(self, cached_note_type: type[TNote], note_constructor: Callable[[JPNoteData], TNote]) -> None:
        self._note_constructor: Callable[[JPNoteData], TNote] = note_constructor
        self._note_type: type[TNote] = cached_note_type
        self._by_id: dict[JPNoteId, TNote] = {}

        self._update_listeners: list[Callable[[TNote], None]] = []

    def on_note_updated(self, listener: Callable[[TNote], None]) -> None:
        self._update_listeners.append(listener)

    def with_id_or_none(self, note_id: JPNoteId) -> TNote | None:
        return self._by_id.get(note_id, None)

    def anki_note_updated(self, note: TNote) -> None:
        self._refresh_in_cache(note)

    def jp_note_updated(self, note: TNote) -> None:
        self._refresh_in_cache(note)
        self._notify_update_listeners(note)

    def _notify_update_listeners(self, note: TNote) -> None:
        for listener in self._update_listeners: listener(note)

    def _refresh_in_cache(self, note: TNote) -> None:
        self.remove_from_cache(note)
        self.add_to_cache(note)

    def init_from_list(self, all_notes: list[JPNoteData]) -> None:
        if len(all_notes) > 0:
            with TaskRunner.current(f"Pushing {self._note_type.__name__} notes into cache") as task_runner:
                task_runner.process_with_progress(all_notes, self._add_to_cache_from_data, f"Pushing {self._note_type.__name__} notes into cache")

    def _add_to_cache_from_data(self, note_data: JPNoteData) -> None:
        self.add_to_cache(self._note_constructor(note_data))

    def remove_from_cache(self, note: TNote) -> None: raise AbstractMethodCalledError()  # pyright: ignore[reportUnusedParameter]
    def add_to_cache(self, note: TNote) -> None: raise AbstractMethodCalledError()  # pyright: ignore[reportUnusedParameter]

    def set_studying_statuses(self, card_statuses: list[CardStudyingStatus]) -> None:
        for status in card_statuses:
            note = self.with_id_or_none(status.note_id)
            if note is not None:
                note.set_studying_status(status)

class NoteCache[TNote: JPNote, TSnapshot: CachedNote](NoteCacheBase[TNote], Slots):
    def __init__(self, cached_note_type: type[TNote], note_constructor: Callable[[JPNoteData], TNote]) -> None:
        super().__init__(cached_note_type, note_constructor)
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets
        self._by_question: DefaultDictCaseInsensitive[QList[TNote]] = DefaultDictCaseInsensitive(QList[TNote])
        self._snapshot_by_id: dict[JPNoteId, TSnapshot] = {}

        self._deleted: QSet[JPNoteId] = QSet()

        self._flushing: bool = False

    def all(self) -> QList[TNote]:
        return QList(self._by_id.values())

    def with_question(self, question: str) -> QList[TNote]:
        return self._by_question.get_value_or_default(question).to_list()

    def _create_snapshot(self, note: TNote) -> TSnapshot: raise AbstractMethodCalledError()  # pyright: ignore[reportUnusedParameter]
    def _inheritor_remove_from_cache(self, note: TNote, snapshot: TSnapshot) -> None: raise AbstractMethodCalledError()  # pyright: ignore[reportUnusedParameter]
    def _inheritor_add_to_cache(self, note: TNote, snapshot: TSnapshot) -> None: raise AbstractMethodCalledError()  # pyright: ignore[reportUnusedParameter]

    @override
    def remove_from_cache(self, note: TNote) -> None:
        assert note.get_id()
        cached = self._snapshot_by_id.pop(note.get_id())
        self._by_id.pop(note.get_id())
        self._by_question[cached.question].remove(note)
        self._inheritor_remove_from_cache(note, cached)

    _next_note_id: JPNoteId = 1
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
