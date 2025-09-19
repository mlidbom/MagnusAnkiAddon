from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, override

from anki_extentions.note_ex import NoteBulkLoader
from ex_autoslot import AutoSlots
from line_profiling_hacks import profile_lines
from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.note_constants import NoteTypes
from note.vocabulary.vocabnote import VocabNote
from sysutils.collections.linq.q_iterable import QList, query

if TYPE_CHECKING:
    from collections.abc import Iterable

    from anki.collection import Collection
    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner
    from note.kanjinote import KanjiNote
    from qt_utils.task_runner_progress_dialog import ITaskRunner

class _VocabSnapshot(CachedNote, AutoSlots):
    def __init__(self, note: VocabNote) -> None:
        super().__init__(note)
        self.forms: set[str] = set(note.forms.all_set())
        self.compound_parts: set[str] = set(note.compound_parts.all())
        self.main_form_kanji: set[str] = set(note.kanji.extract_main_form_kanji())
        self.all_kanji: set[str] = note.kanji.extract_all_kanji()
        self.readings: set[str] = set(note.readings.get())
        self.derived_from: str = note.related_notes.derived_from.get()
        self.stems: list[str] = note.conjugator.get_stems_for_primary_form()

class _VocabCache(NoteCache[VocabNote, _VocabSnapshot], AutoSlots):
    @profile_lines
    def __init__(self, all_vocab: list[VocabNote], cache_runner: CacheRunner, task_runner: ITaskRunner) -> None:
        self._by_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_kanji_in_main_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_kanji_in_any_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_compound_part: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_derived_from: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_reading: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_stem: dict[str, set[VocabNote]] = defaultdict(set)
        super().__init__(all_vocab, VocabNote, cache_runner, task_runner)

    def with_form(self, form: str) -> QList[VocabNote]: return QList(self._by_form[form]) if form in self._by_form else QList[VocabNote]()

    def with_compound_part(self, form: str) -> list[VocabNote]:
        compound_parts: set[VocabNote] = set()

        def fetch_parts(part_form: str) -> None:
            for vocab in self._by_compound_part[part_form]:
                if vocab not in compound_parts:
                    compound_parts.add(vocab)
                    fetch_parts(vocab.get_question())

        fetch_parts(form)

        def get_vocab_question(vocab: VocabNote) -> str: return vocab.get_question()
        return sorted(compound_parts, key=get_vocab_question)

    def derived_from(self, form: str) -> list[VocabNote]: return list(self._by_derived_from[form])
    def with_kanji_in_main_form(self, kanji: str) -> list[VocabNote]: return list(self._by_kanji_in_main_form[kanji])
    def with_kanji_in_any_form(self, kanji: str) -> list[VocabNote]: return list(self._by_kanji_in_any_form[kanji])
    def with_reading(self, reading: str) -> list[VocabNote]: return list(self._by_reading[reading])
    def with_stem(self, stem: str) -> list[VocabNote]: return list(self._by_stem[stem])

    @override
    def _create_snapshot(self, note: VocabNote) -> _VocabSnapshot: return _VocabSnapshot(note)

    @override
    def _inheritor_remove_from_cache(self, note: VocabNote, snapshot: _VocabSnapshot) -> None:
        for form in snapshot.forms: self._by_form[form].remove(note)
        for part in snapshot.compound_parts: self._by_compound_part[part].remove(note)
        self._by_derived_from[snapshot.derived_from].remove(note)
        for kanji in snapshot.main_form_kanji: self._by_kanji_in_main_form[kanji].remove(note)
        for kanji in snapshot.all_kanji: self._by_kanji_in_any_form[kanji].remove(note)
        for kanji in snapshot.readings: self._by_reading[kanji].remove(note)
        for stem in snapshot.stems: self._by_stem[stem].remove(note)

    @override
    def _inheritor_add_to_cache(self, note: VocabNote, snapshot: _VocabSnapshot) -> None:
        for form in snapshot.forms: self._by_form[form].add(note)
        for compound_part in snapshot.compound_parts: self._by_compound_part[compound_part].add(note)
        # todo: We add these regardless of whether they have a value in derived from? Won't there be a ton of instances for the empty string?
        self._by_derived_from[snapshot.derived_from].add(note)
        for kanji in snapshot.main_form_kanji: self._by_kanji_in_main_form[kanji].add(note)
        for kanji in snapshot.all_kanji: self._by_kanji_in_any_form[kanji].add(note)
        for reading in snapshot.readings: self._by_reading[reading].add(note)
        for stem in snapshot.stems: self._by_stem[stem].add(note)

class VocabCollection(AutoSlots):
    @profile_lines
    def __init__(self, collection: Collection, cache_manager: CacheRunner, task_runner: ITaskRunner) -> None:
        def vocab_constructor_call_while_populating_vocab_collection(note: Note) -> VocabNote: return VocabNote(note)
        self.collection: BackEndFacade[VocabNote] = BackEndFacade[VocabNote](collection, vocab_constructor_call_while_populating_vocab_collection, NoteTypes.Vocab)
        all_vocab = self.collection.all(task_runner)
        self._cache: _VocabCache = _VocabCache(all_vocab, cache_manager, task_runner)

    def search(self, query: str) -> list[VocabNote]: return list(self.collection.search(query))

    def all_old(self, task_runner: ITaskRunner) -> list[VocabNote]:
        backend_notes = NoteBulkLoader.load_all_notes_of_type(self.collection.anki_collection, NoteTypes.Vocab, task_runner)
        return [VocabNote(backend_note) for backend_note in backend_notes]

    def is_word(self, form: str) -> bool: return any(self._cache.with_form(form))
    def all(self) -> list[VocabNote]: return self._cache.all()
    def with_id_or_none(self, note_id: NoteId) -> VocabNote | None: return self._cache.with_id_or_none(note_id)
    def with_form(self, form: str) -> QList[VocabNote]: return self._cache.with_form(form)
    def with_compound_part(self, compound_part: str) -> list[VocabNote]: return self._cache.with_compound_part(compound_part)
    def derived_from(self, derived_from: str) -> list[VocabNote]: return self._cache.derived_from(derived_from)
    def with_kanji_in_main_form(self, kanji: KanjiNote) -> list[VocabNote]: return self._cache.with_kanji_in_main_form(kanji.get_question())
    def with_kanji_in_any_form(self, kanji: KanjiNote) -> list[VocabNote]: return self._cache.with_kanji_in_any_form(kanji.get_question())
    def with_question(self, question: str) -> QList[VocabNote]: return self._cache.with_question(question)
    def with_reading(self, question: str) -> list[VocabNote]: return self._cache.with_reading(question)
    def with_stem(self, question: str) -> list[VocabNote]: return self._cache.with_stem(question)

    def with_form_prefer_exact_match(self, form: str) -> list[VocabNote]:
        matches: list[VocabNote] = self.with_form(form)
        exact_match = [voc for voc in matches if voc.question.without_noise_characters == form]
        sequence = exact_match if exact_match else matches
        return query(sequence).distinct().to_list()

    def with_any_form_in_prefer_exact_match(self, forms: list[str]) -> QList[VocabNote]:
        return query(forms).select_many(self.with_form_prefer_exact_match).distinct().to_list()  #ex_sequence.remove_duplicates_while_retaining_order(ex_sequence.flatten([self.with_form_prefer_exact_match(form) for form in forms]))

    def with_any_form_in(self, forms: list[str]) -> list[VocabNote]:
        return query(forms).select_many(self.with_form).distinct().to_list()  #ex_sequence.remove_duplicates_while_retaining_order(ex_sequence.flatten([self.with_form(form) for form in forms]))

    def with_any_question_in(self, questions: Iterable[str]) -> QList[VocabNote]:
        return query(questions).select(self.with_question).select_many(lambda x: x).to_list()

    def add(self, note: VocabNote) -> None:
        self.collection.anki_collection.addNote(note.backend_note)
        self._cache.add_note_to_cache(note)
