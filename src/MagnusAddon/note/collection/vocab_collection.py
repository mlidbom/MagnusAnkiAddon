from __future__ import annotations

from collections import defaultdict
from typing import Any

from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from note.vocabnote import VocabNote
from sysutils.lazy import Lazy

class _CachedVocab(CachedNote):
    def __init__(self, note: VocabNote):
        super().__init__(note)
        self.question = note.get_question()
        self.forms = note.get_forms()
        self.kanji = note.extract_kanji()

class _VocabCache(NoteCache[VocabNote, _CachedVocab]):
    def __init__(self, all_vocab: list[VocabNote]):
        super().__init__(all_vocab, VocabNote)
        self._by_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_kanji: dict[str, set[VocabNote]] = defaultdict(set)

    def all(self) -> list[VocabNote]: return list(self._merged_self()._by_id.values())
    def with_form(self, form: str) -> list[VocabNote]: return list(self._merged_self()._by_form[form])
    def with_kanji(self, kanji: str) -> list[VocabNote]: return list(self._merged_self()._by_kanji[kanji])

    def _create_cached_note(self, note: VocabNote) -> _CachedVocab: return _CachedVocab(note)

    def _inheritor_remove_from_cache(self, note: VocabNote, cached:_CachedVocab) -> None:
        for form in cached.forms: self._by_form[form].discard(note)
        for kanji in cached.kanji: self._by_kanji[kanji].discard(note)

    def _inheritor_add_to_cache(self, note: VocabNote) -> None:
        for form in note.get_forms(): self._by_form[form].add(note)
        for kanji in note.extract_kanji(): self._by_kanji[kanji].add(note)

class VocabCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection
        self._cache_factory = Lazy(lambda: _VocabCache(self._all_internal()))

    def _cache(self) -> _VocabCache: return self._cache_factory.instance()

    def search(self, query: str) -> list[VocabNote]:
        return [VocabNote(note) for note in (self.collection.search_notes(query))]

    def all_wani(self) -> list[VocabNote]:
        return [vocab for vocab in self.all() if vocab.is_wani_note()]

    def _all_internal(self) -> list[VocabNote]:
        notes = self.collection.fetch_notes_by_note_type(NoteTypes.Vocab)
        vocab_notes = [VocabNote(note) for note in notes]
        return vocab_notes

    def all(self) -> list[VocabNote]: return self._cache().all()
    def with_form(self, form: str) -> list[VocabNote]: return self._cache().with_form(form)
    def with_kanji(self, kanji: KanjiNote) -> list[VocabNote]: return self._cache().with_kanji(kanji.get_question())
