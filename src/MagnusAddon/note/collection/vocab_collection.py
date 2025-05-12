from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.note_constants import NoteTypes
from note.vocabulary.vocabnote import VocabNote

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner
    from note.kanjinote import KanjiNote



class _VocabSnapshot(CachedNote):
    def __init__(self, note: VocabNote) -> None:
        super().__init__(note)
        self.forms = set(note.get_forms())
        self.compound_parts = set(note.get_user_compounds())
        self.main_form_kanji = set(note.extract_main_form_kanji())
        self.all_kanji = note.extract_all_kanji()
        self.readings = set(note.get_readings())
        self.derived_from = note.related_notes.derived_from.get()
        self.stems = note.get_stems_for_primary_form()

class _VocabCache(NoteCache[VocabNote, _VocabSnapshot]):
    def __init__(self, all_vocab: list[VocabNote], cache_runner: CacheRunner) -> None:
        self._by_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_kanji_in_main_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_kanji_in_any_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_compound_part: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_derived_from: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_reading: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_stem: dict[str, set[VocabNote]] = defaultdict(set)
        super().__init__(all_vocab, VocabNote, cache_runner)

    def with_form(self, form: str) -> list[VocabNote]: return list(self._by_form[form]) if form in self._by_form else []

    def with_compound_part(self, form: str) -> list[VocabNote]:
        compound_parts: set[VocabNote] = set()

        def fetch_parts(part_form: str) -> None:
            for vocab in self._by_compound_part[part_form]:
                if vocab not in compound_parts:
                    compound_parts.add(vocab)
                    fetch_parts(vocab.get_question())

        fetch_parts(form)

        return sorted(compound_parts, key=lambda part: part.get_question())

    def derived_from(self, form: str) -> list[VocabNote]: return list(self._by_derived_from[form])
    def with_kanji_in_main_form(self, kanji: str) -> list[VocabNote]: return list(self._by_kanji_in_main_form[kanji])
    def with_kanji_in_any_form(self, kanji: str) -> list[VocabNote]: return list(self._by_kanji_in_any_form[kanji])
    def with_reading(self, reading: str) -> list[VocabNote]: return list(self._by_reading[reading])
    def with_stem(self, stem: str) -> list[VocabNote]: return list(self._by_stem[stem])

    def _create_snapshot(self, note: VocabNote) -> _VocabSnapshot: return _VocabSnapshot(note)

    def _inheritor_remove_from_cache(self, note: VocabNote, cached:_VocabSnapshot) -> None:
        for form in cached.forms: self._by_form[form].remove(note)
        for part in cached.compound_parts: self._by_compound_part[part].remove(note)
        self._by_derived_from[cached.derived_from].remove(note)
        for kanji in cached.main_form_kanji: self._by_kanji_in_main_form[kanji].remove(note)
        for kanji in cached.all_kanji: self._by_kanji_in_any_form[kanji].remove(note)
        for kanji in cached.readings: self._by_reading[kanji].remove(note)
        for stem in cached.stems: self._by_stem[stem].remove(note)

    def _inheritor_add_to_cache(self, note: VocabNote) -> None:
        for form in note.get_forms(): self._by_form[form].add(note)
        for compound_part in note.get_user_compounds(): self._by_compound_part[compound_part].add(note)
        self._by_derived_from[note.related_notes.derived_from.get()].add(note)
        for kanji in note.extract_main_form_kanji(): self._by_kanji_in_main_form[kanji].add(note)
        for kanji in note.extract_all_kanji(): self._by_kanji_in_any_form[kanji].add(note)
        for reading in note.get_readings(): self._by_reading[reading].add(note)
        for stem in note.get_stems_for_primary_form(): self._by_stem[stem].add(note)

class VocabCollection:
    def __init__(self, collection: Collection, cache_manager: CacheRunner) -> None:
        def vocab_constructor(note: Note) -> VocabNote: return VocabNote(note)
        self.collection = BackEndFacade[VocabNote](collection, vocab_constructor, NoteTypes.Vocab)
        self._cache = _VocabCache(list(self.collection.all()), cache_manager)

    def search(self, query: str) -> list[VocabNote]: return list(self.collection.search(query))

    def all_wani(self) -> list[VocabNote]:
        return [vocab for vocab in self.all() if vocab.is_wani_note()]

    def is_word(self, form: str) -> bool: return any(self._cache.with_form(form))
    def all(self) -> list[VocabNote]: return self._cache.all()
    def with_id(self, note_id:NoteId) -> VocabNote: return self._cache.with_id(note_id)
    def with_form(self, form: str) -> list[VocabNote]: return self._cache.with_form(form)
    def with_compound_part(self, compound_part: str) -> list[VocabNote]: return self._cache.with_compound_part(compound_part)
    def derived_from(self, derived_from: str) -> list[VocabNote]: return self._cache.derived_from(derived_from)
    def with_kanji_in_main_form(self, kanji: KanjiNote) -> list[VocabNote]: return self._cache.with_kanji_in_main_form(kanji.get_question())
    def with_kanji_in_any_form(self, kanji: KanjiNote) -> list[VocabNote]: return self._cache.with_kanji_in_any_form(kanji.get_question())
    def with_question(self, question: str) -> list[VocabNote]: return self._cache.with_question(question)
    def with_reading(self, question: str) -> list[VocabNote]: return self._cache.with_reading(question)
    def with_stem(self, question: str) -> list[VocabNote]: return self._cache.with_stem(question)
