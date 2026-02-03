from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots
from typed_linq_collections.collections.q_default_dict import QDefaultDict
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from typed_linq_collections.collections.q_set import QSet

    from jaslib.note.jpnote import JPNoteId

from typed_linq_collections.collections.q_list import QList

from jaslib.note.collection.note_cache import CachedNote, NoteCache
from jaslib.note.kanjinote import KanjiNote
from jaslib.sysutils import kana_utils


@final
class _KanjiSnapshot(CachedNote, Slots):
    def __init__(self, note: KanjiNote) -> None:
        super().__init__(note)
        self.radicals: tuple[str, ...] = note.get_radicals().to_set().to_tuple()
        self.readings: tuple[str, ...] = note.get_readings_clean().to_set().to_tuple()

class _KanjiCache(NoteCache[KanjiNote, _KanjiSnapshot], Slots):
    def __init__(self) -> None:
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets
        self._by_radical: QDefaultDict[str, QList[KanjiNote]] = QDefaultDict(QList[KanjiNote])
        self.by_reading: QDefaultDict[str, QList[KanjiNote]] = QDefaultDict(QList[KanjiNote])
        super().__init__(KanjiNote, KanjiNote)

    @override
    def _create_snapshot(self, note: KanjiNote) -> _KanjiSnapshot: return _KanjiSnapshot(note)

    @classmethod
    def remove_first_note_with_id(cls, note_list: list[KanjiNote], id: JPNoteId) -> None:
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
    def __init__(self) -> None:
        self.cache: _KanjiCache = _KanjiCache()

    def all(self) -> QList[KanjiNote]: return self.cache.all()

    def with_id_or_none(self, note_id:JPNoteId) -> KanjiNote | None:
        return self.cache.with_id_or_none(note_id)

    def with_any_kanji_in(self, kanji_list: list[str]) -> QList[KanjiNote]:
        return query(kanji_list).select_many(self.cache.with_question).to_list()

    def with_kanji(self, kanji: str) -> KanjiNote | None:
        return self.cache.with_question(kanji).single_or_none()

    # noinspection PyUnusedFunction
    def with_radical(self, radical:str) -> QList[KanjiNote]: return self.cache.with_radical(radical)
    # noinspection PyUnusedFunction
    def with_reading(self, reading:str) -> QSet[KanjiNote]:
        return self.cache.by_reading.get_value_or_default(kana_utils.anything_to_hiragana(reading)).to_set()

    def add(self, note: KanjiNote) -> None:
        self.cache.add_to_cache(note)