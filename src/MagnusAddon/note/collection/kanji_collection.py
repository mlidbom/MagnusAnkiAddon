from __future__ import annotations

from typing import List

from note.note_constants import NoteFields

from collections import defaultdict
from typing import Self, Sequence

from anki import hooks
from anki.collection import Collection
from anki.notes import Note, NoteId

from note.collection.backend_facade import BackEndFacade
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from sysutils import ex_sequence
from sysutils.lazy import Lazy

class _CachedKanji:
    def __init__(self, note: KanjiNote):
        self.id = note.get_id()
        self.question = note.get_question()

class _Cache:
    def __init__(self, all_kanji: list[KanjiNote]):
        self._by_question: dict[str, set[KanjiNote]] = defaultdict(set)
        self._by_id: dict[NoteId, KanjiNote] = {}
        self._cached_by_id: dict[NoteId, _CachedKanji] = {}
        self._pending_add: list[KanjiNote] = []

        for kanji in all_kanji:
            self._add_to_cache(kanji)

        self._setup_hooks()

    def all(self) -> list[KanjiNote]: return list(self._merged_self()._by_id.values())
    def with_kanji(self, kanji: str) -> list[KanjiNote]: return list(self._merged_self()._by_question[kanji])

    def _merge_pending(self) -> None:
        added_kanji = [v for v in self._pending_add if v.get_id()]
        self._pending_add = [v for v in self._pending_add if not v.get_id()]
        for kanji in added_kanji:
            self._add_to_cache(kanji)

    def _merged_self(self) -> Self:
        self._merge_pending()
        return self

    def _setup_hooks(self) -> None:
        hooks.notes_will_be_deleted.append(self._on_will_be_removed)
        hooks.note_will_flush.append(self._on_will_flush)

    def _on_will_be_removed(self, _: Collection, note_ids: Sequence[NoteId]) -> None:
        cached_notes = [self._by_id[note_id] for note_id in note_ids if note_id in self._cached_by_id]
        for cached in cached_notes:
            self._remove_from_cache(cached)

    # noinspection DuplicatedCode
    def _on_will_flush(self, backend_note: Note) -> None:
        note = JPNote.note_from_note(backend_note)
        if isinstance(note, KanjiNote):
            if note.get_id():
                if note.get_id() in self._by_id:
                    self._remove_from_cache(note)

                self._add_to_cache(note)
            else:
                self._pending_add.append(note)

    def _remove_from_cache(self, note: KanjiNote) -> None:
        assert note.get_id()
        cached = self._cached_by_id.pop(note.get_id())
        self._by_id.pop(note.get_id())
        self._by_question[cached.question].discard(note)

    def _add_to_cache(self, note: KanjiNote) -> None:
        assert note.get_id()
        self._by_id[note.get_id()] = note
        self._cached_by_id[note.get_id()] = _CachedKanji(note)
        self._by_question[note.get_question()].add(note)

class KanjiCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection
        self._cache_factory = Lazy(lambda: _Cache(self._all_internal()))

    def search(self, query: str) -> list[KanjiNote]:
        return [KanjiNote(note) for note in self.collection.search_notes(query)]

    def _all_internal(self) -> List[KanjiNote]:
        notes = self.collection.fetch_notes_by_note_type(NoteTypes.Kanji)
        kanji_notes = [KanjiNote(note) for note in notes]
        return kanji_notes

    def all(self) -> list[KanjiNote]: return self._cache().all()

    def all_wani(self) -> list[KanjiNote]:
        return [kanji for kanji in self.all() if kanji.is_wani_note()]

    def by_kanji(self, kanji_list: list[str]) -> List[KanjiNote]:
        return ex_sequence.flatten([self._cache().with_kanji(kanji) for kanji in kanji_list])

    def _cache(self) -> _Cache: return self._cache_factory.instance()
