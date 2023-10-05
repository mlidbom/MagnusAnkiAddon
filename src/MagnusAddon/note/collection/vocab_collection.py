from __future__ import annotations

from collections import defaultdict

from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from note.vocabnote import VocabNote

class _VocabSnapshot(CachedNote):
    def __init__(self, note: VocabNote):
        super().__init__(note)
        self.question = note.get_question()
        self.forms = note.get_forms()
        self.kanji = note.extract_kanji()

class _VocabCache(NoteCache[VocabNote, _VocabSnapshot]):
    def __init__(self, all_vocab: list[VocabNote]):
        self._by_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_kanji: dict[str, set[VocabNote]] = defaultdict(set)
        super().__init__(all_vocab, VocabNote)

    def all(self) -> list[VocabNote]: return list(self._merged_self()._by_id.values())
    def with_form(self, form: str) -> list[VocabNote]: return list(self._merged_self()._by_form[form])
    def with_kanji(self, kanji: str) -> list[VocabNote]: return list(self._merged_self()._by_kanji[kanji])

    def _create_snapshot(self, note: VocabNote) -> _VocabSnapshot: return _VocabSnapshot(note)

    def _inheritor_remove_from_cache(self, note: VocabNote, cached:_VocabSnapshot) -> None:
        for form in cached.forms: self._by_form[form].discard(note)
        for kanji in cached.kanji: self._by_kanji[kanji].discard(note)

    def _inheritor_add_to_cache(self, note: VocabNote) -> None:
        for form in note.get_forms(): self._by_form[form].add(note)
        for kanji in note.extract_kanji(): self._by_kanji[kanji].add(note)

class VocabCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection
        self._cache = _VocabCache([VocabNote(note) for note in (self.collection.fetch_notes_by_note_type(NoteTypes.Vocab))])

    def search(self, query: str) -> list[VocabNote]:
        return [VocabNote(note) for note in (self.collection.search_notes(query))]

    def all_wani(self) -> list[VocabNote]:
        return [vocab for vocab in self.all() if vocab.is_wani_note()]

    def all(self) -> list[VocabNote]: return self._cache.all()
    def with_form(self, form: str) -> list[VocabNote]: return self._cache.with_form(form)
    def with_kanji(self, kanji: KanjiNote) -> list[VocabNote]: return self._cache.with_kanji(kanji.get_question())
