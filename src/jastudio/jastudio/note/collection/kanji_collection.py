from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from typed_linq_collections.collections.q_default_dict import QDefaultDict
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import Note, NoteId
    from jastudio.note.collection.cache_runner import CacheRunner
    from typed_linq_collections.collections.q_set import QSet

from jastudio.note.collection.backend_facade import BackEndFacade
from jastudio.note.collection.note_cache import CachedNote, NoteCache
from jastudio.note.kanjinote import KanjiNote
from jastudio.note.note_constants import NoteTypes
from jastudio.sysutils import kana_utils
from typed_linq_collections.collections.q_list import QList


@final
class _KanjiSnapshot(CachedNote, Slots):
    def __init__(self, note: KanjiNote) -> None:
        super().__init__(note)
        self.radicals: tuple[str, ...] = note.get_radicals().to_set().to_tuple()
        self.readings: tuple[str, ...] = note.get_readings_clean().to_set().to_tuple()

class _KanjiCache(NoteCache[KanjiNote, _KanjiSnapshot], Slots):
    def __init__(self, all_kanji: list[KanjiNote], cache_runner: CacheRunner) -> None:
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets
        self._by_radical: QDefaultDict[str, QList[KanjiNote]] = QDefaultDict(QList[KanjiNote])
        self.by_reading: QDefaultDict[str, QList[KanjiNote]] = QDefaultDict(QList[KanjiNote])
        super().__init__(all_kanji, KanjiNote, cache_runner)

    @override
    def _create_snapshot(self, note: KanjiNote) -> _KanjiSnapshot: return _KanjiSnapshot(note)

    @classmethod
    def remove_first_note_with_id(cls, note_list: list[KanjiNote], id: NoteId) -> None:
        for index, note in enumerate(note_list):
            if note.get_id() == id:
                del note_list[index]
                return
        raise Exception(f"Could not find note with id {id} in list {note_list}")

    @override
    def _inheritor_remove_from_cache(self, note: KanjiNote, snapshot:_KanjiSnapshot) -> None:
        id = snapshot.id
        for form in snapshot.radicals: self.remove_first_note_with_id(self._by_radical[form], id)
        for reading in snapshot.readings: self.remove_first_note_with_id(self.by_reading[reading], id)

    @override
    def _inheritor_add_to_cache(self, note: KanjiNote, snapshot: _KanjiSnapshot) -> None:
        for form in snapshot.radicals: self._by_radical[form].append(note)
        for reading in snapshot.readings: self.by_reading[reading].append(note)

    def with_radical(self, radical: str) -> QList[KanjiNote]: return self._by_radical.get_value_or_default(radical).to_list()

class KanjiCollection(Slots):
    def __init__(self, collection: Collection, cache_manager: CacheRunner) -> None:
        def kanji_constructor_call_while_populating_kanji_collection(note: Note) -> KanjiNote: return KanjiNote(note)
        self.collection: BackEndFacade[KanjiNote] = BackEndFacade[KanjiNote](collection, kanji_constructor_call_while_populating_kanji_collection, NoteTypes.Kanji)
        all_kanji = self.collection.all()
        self._cache: _KanjiCache = _KanjiCache(all_kanji, cache_manager)

    def all(self) -> QList[KanjiNote]: return self._cache.all()

    def with_id_or_none(self, note_id:NoteId) -> KanjiNote | None:
        return self._cache.with_id_or_none(note_id)

    def with_any_kanji_in(self, kanji_list: list[str]) -> QList[KanjiNote]:
        return query(kanji_list).select_many(self._cache.with_question).to_list()  # ex_sequence.flatten([self._cache.with_question(kanji) for kanji in kanji_list])

    def with_kanji(self, kanji: str) -> KanjiNote | None:
        return self._cache.with_question(kanji).single_or_none()

    def with_radical(self, radical:str) -> QList[KanjiNote]: return self._cache.with_radical(radical)
    def with_reading(self, reading:str) -> QSet[KanjiNote]:
        return self._cache.by_reading.get_value_or_default(kana_utils.anything_to_hiragana(reading)).to_set()

    def add(self, note: KanjiNote) -> None:
        self.collection.anki_collection.addNote(note.backend_note)
        self._cache.add_note_to_cache(note)