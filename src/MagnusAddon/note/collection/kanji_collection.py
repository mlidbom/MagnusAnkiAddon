from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, final, override

from autoslot import Slots

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner
    from qt_utils.task_runner_progress_dialog import ITaskRunner

from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from sysutils import ex_sequence, kana_utils


@final
class _KanjiSnapshot(CachedNote, Slots):
    def __init__(self, note: KanjiNote) -> None:
        super().__init__(note)
        self.radicals: set[str] = set(note.get_radicals())
        self.readings: set[str] = set(note.get_readings_clean())

class _KanjiCache(NoteCache[KanjiNote, _KanjiSnapshot], Slots):
    def __init__(self, all_kanji: list[KanjiNote], cache_runner: CacheRunner, task_runner: ITaskRunner) -> None:
        self._by_radical: dict[str, set[KanjiNote]] = defaultdict(set)
        self.by_reading: dict[str, set[KanjiNote]] = defaultdict(set)
        super().__init__(all_kanji, KanjiNote, cache_runner, task_runner)

    @override
    def _create_snapshot(self, note: KanjiNote) -> _KanjiSnapshot: return _KanjiSnapshot(note)

    @override
    def _inheritor_remove_from_cache(self, note: KanjiNote, snapshot:_KanjiSnapshot) -> None:
        for form in snapshot.radicals: self._by_radical[form].remove(note)
        for reading in snapshot.readings: self.by_reading[reading].remove(note)

    @override
    def _inheritor_add_to_cache(self, note: KanjiNote, snapshot: _KanjiSnapshot) -> None:
        for form in snapshot.radicals: self._by_radical[form].add(note)
        for reading in snapshot.readings: self.by_reading[reading].add(note)

    def with_radical(self, radical: str) -> list[KanjiNote]: return list(self._by_radical[radical])

class KanjiCollection(Slots):
    def __init__(self, collection: Collection, cache_manager: CacheRunner, task_runner: ITaskRunner) -> None:
        def kanji_constructor(note: Note) -> KanjiNote: return KanjiNote(note)
        self.collection: BackEndFacade[KanjiNote] = BackEndFacade[KanjiNote](collection, kanji_constructor, NoteTypes.Kanji)
        all_kanji = self.collection.all(task_runner)
        self._cache: _KanjiCache = _KanjiCache(all_kanji, cache_manager, task_runner)

    def search(self, query: str) -> list[KanjiNote]:
        return list(self.collection.search(query))

    def all(self) -> list[KanjiNote]: return self._cache.all()

    def all_old(self, task_runner: ITaskRunner) -> list[KanjiNote]:
        return self.collection.all_old(task_runner)

    def with_id_or_none(self, note_id:NoteId) -> KanjiNote | None:
        return self._cache.with_id_or_none(note_id)

    def all_wani(self) -> list[KanjiNote]:
        return [kanji for kanji in self.all() if kanji.is_wani_note()]

    def with_any_kanji_in(self, kanji_list: list[str]) -> list[KanjiNote]:
        return ex_sequence.flatten([self._cache.with_question(kanji) for kanji in kanji_list])

    def with_kanji(self, kanji: str) -> KanjiNote | None:
        found = self._cache.with_question(kanji)
        return found[0] if found else None

    def with_radical(self, radical:str) -> list[KanjiNote]: return self._cache.with_radical(radical)
    def with_reading(self, reading:str) -> set[KanjiNote]:
        return self._cache.by_reading[kana_utils.anything_to_hiragana(reading)]