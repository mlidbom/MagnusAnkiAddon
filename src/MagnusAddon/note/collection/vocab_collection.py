from __future__ import annotations

from collections import defaultdict

from anki.collection import Collection
from anki.notes import Note, NoteId

from note.collection.backend_facade import BackEndFacade
from note.collection.cache_runner import CacheRunner
from note.collection.note_cache import CachedNote, NoteCache
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from note.vocabnote import VocabNote
from sysutils import ex_sequence

class _VocabSnapshot(CachedNote):
    def __init__(self, note: VocabNote):
        super().__init__(note)
        self.forms = set(note.get_forms())
        self.kanji = set(note.extract_kanji())
        self.readings = set(note.get_readings())

class _VocabCache(NoteCache[VocabNote, _VocabSnapshot]):
    def __init__(self, all_vocab: list[VocabNote], cache_runner: CacheRunner):
        self._by_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_kanji: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_reading: dict[str, set[VocabNote]] = defaultdict(set)
        super().__init__(all_vocab, VocabNote, cache_runner)

    def with_form(self, form: str) -> list[VocabNote]: return list(self._by_form[form])
    def with_kanji(self, kanji: str) -> list[VocabNote]: return list(self._by_kanji[kanji])
    def with_reading(self, reading: str) -> list[VocabNote]: return list(self._by_reading[reading])

    def _create_snapshot(self, note: VocabNote) -> _VocabSnapshot: return _VocabSnapshot(note)

    def _inheritor_remove_from_cache(self, note: VocabNote, cached:_VocabSnapshot) -> None:
        #todo: this should really be handled by an event or something but...
        from ankiutils import app
        kanji_notes = app.col().kanji.with_any_kanji_in(note.extract_kanji())
        for kanji_note in kanji_notes:
            kanji_note.update_generated_data()

        for form in cached.forms: self._by_form[form].remove(note)
        for kanji in cached.kanji: self._by_kanji[kanji].remove(note)
        for kanji in cached.readings: self._by_reading[kanji].remove(note)

    def _inheritor_add_to_cache(self, note: VocabNote) -> None:
        for form in note.get_forms(): self._by_form[form].add(note)
        for kanji in note.extract_kanji(): self._by_kanji[kanji].add(note)
        for reading in note.get_readings(): self._by_reading[reading].add(note)

class VocabCollection:
    def __init__(self, collection: Collection, cache_manager: CacheRunner):
        def vocab_constructor(note: Note) -> VocabNote: return VocabNote(note)
        self.collection = BackEndFacade[VocabNote](collection, vocab_constructor, NoteTypes.Vocab)
        self._cache = _VocabCache(list(self.collection.all()), cache_manager)

    def search(self, query: str) -> list[VocabNote]: return list(self.collection.search(query))

    def all_wani(self) -> list[VocabNote]:
        return [vocab for vocab in self.all() if vocab.is_wani_note()]

    def all(self) -> list[VocabNote]: return self._cache.all()
    def with_id(self, note_id:NoteId) -> VocabNote: return self._cache.with_id(note_id)
    def with_form(self, form: str) -> list[VocabNote]: return self._cache.with_form(form)
    def with_forms(self, forms: list[str]) -> list[VocabNote]: return ex_sequence.flatten([self.with_form(form) for form in forms])
    def with_kanji(self, kanji: KanjiNote) -> list[VocabNote]: return self._cache.with_kanji(kanji.get_question())
    def with_question(self, question: str) -> list[VocabNote]: return self._cache.with_question(question)
    def with_reading(self, question: str) -> list[VocabNote]: return self._cache.with_reading(question)
