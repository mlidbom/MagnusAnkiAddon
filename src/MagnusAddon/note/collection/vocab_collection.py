from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, override

from autoslot import Slots
from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.note_constants import NoteTypes
from note.vocabulary.vocabnote import VocabNote
from typed_linq_collections.collections.q_default_dict import QDefaultDict  # pyright: ignore [reportMissingTypeStubs]
from typed_linq_collections.collections.q_list import QList
from typed_linq_collections.collections.q_set import QSet
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from collections.abc import Iterable

    from anki.collection import Collection
    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner
    from note.kanjinote import KanjiNote

class _VocabSnapshot(CachedNote, Slots):
    def __init__(self, note: VocabNote) -> None:
        super().__init__(note)
        self.forms: tuple[str, ...] = note.forms.all_set().to_tuple()
        self.compound_parts: tuple[str, ...] = note.compound_parts.all().to_tuple()
        self.main_form_kanji: tuple[str, ...] = note.kanji.extract_main_form_kanji().to_tuple()
        self.all_kanji: tuple[str, ...] = note.kanji.extract_all_kanji().to_tuple()
        self.readings: tuple[str, ...] = note.readings.get().to_tuple()
        self.derived_from: str = note.related_notes.derived_from.get()
        self.stems: tuple[str, ...] = note.conjugator.get_stems_for_primary_form().to_tuple()

class _VocabCache(NoteCache[VocabNote, _VocabSnapshot], Slots):
    def __init__(self, all_vocab: list[VocabNote], cache_runner: CacheRunner) -> None:
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets
        self._by_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_kanji_in_main_form: QDefaultDict[str, QList[VocabNote]] = QDefaultDict[str, QList[VocabNote]](QList[VocabNote])
        self._by_kanji_in_any_form: QDefaultDict[str, QList[VocabNote]] = QDefaultDict[str, QList[VocabNote]](QList[VocabNote])
        self._by_compound_part: QDefaultDict[str, QList[VocabNote]] = QDefaultDict[str, QList[VocabNote]](QList[VocabNote])
        self._by_derived_from: QDefaultDict[str, QList[VocabNote]] = QDefaultDict[str, QList[VocabNote]](QList[VocabNote])
        self._by_reading: QDefaultDict[str, QList[VocabNote]] = QDefaultDict[str, QList[VocabNote]](QList[VocabNote])
        self._by_stem: QDefaultDict[str, QList[VocabNote]] = QDefaultDict[str, QList[VocabNote]](QList[VocabNote])
        super().__init__(all_vocab, VocabNote, cache_runner)

    def with_form(self, form: str) -> QList[VocabNote]: return QList(self._by_form[form]) if form in self._by_form else QList[VocabNote]()

    def with_compound_part(self, form: str) -> QList[VocabNote]:
        compound_parts: QSet[VocabNote] = QSet()

        def fetch_parts(part_form: str) -> None:
            for vocab in self._by_compound_part.get_value_or_default(part_form):
                if vocab not in compound_parts:
                    compound_parts.add(vocab)
                    fetch_parts(vocab.get_question())

        fetch_parts(form)

        def get_vocab_question(vocab: VocabNote) -> str: return vocab.get_question()
        return compound_parts.order_by(get_vocab_question).to_list()

    def derived_from(self, form: str) -> QList[VocabNote]: return self._by_derived_from.get_value_or_default(form).to_list()
    def with_kanji_in_main_form(self, kanji: str) -> QList[VocabNote]: return self._by_kanji_in_main_form.get_value_or_default(kanji).to_list()
    def with_kanji_in_any_form(self, kanji: str) -> QList[VocabNote]: return self._by_kanji_in_any_form.get_value_or_default(kanji).to_list()
    def with_reading(self, reading: str) -> QList[VocabNote]: return self._by_reading.get_value_or_default(reading).to_list()
    def with_stem(self, stem: str) -> QList[VocabNote]: return self._by_stem.get_value_or_default(stem).to_list()

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
        for compound_part in snapshot.compound_parts: self._by_compound_part[compound_part].append(note)
        # todo: We add these regardless of whether they have a value in derived from? Won't there be a ton of instances for the empty string?
        self._by_derived_from[snapshot.derived_from].append(note)
        for kanji in snapshot.main_form_kanji: self._by_kanji_in_main_form[kanji].append(note)
        for kanji in snapshot.all_kanji: self._by_kanji_in_any_form[kanji].append(note)
        for reading in snapshot.readings: self._by_reading[reading].append(note)
        for stem in snapshot.stems: self._by_stem[stem].append(note)

class VocabCollection(Slots):
    def __init__(self, collection: Collection, cache_manager: CacheRunner) -> None:
        def vocab_constructor_call_while_populating_vocab_collection(note: Note) -> VocabNote: return VocabNote(note)
        self.collection: BackEndFacade[VocabNote] = BackEndFacade[VocabNote](collection, vocab_constructor_call_while_populating_vocab_collection, NoteTypes.Vocab)
        all_vocab = self.collection.all()
        self._cache: _VocabCache = _VocabCache(all_vocab, cache_manager)

    def is_word(self, form: str) -> bool: return any(self._cache.with_form(form))
    def all(self) -> list[VocabNote]: return self._cache.all()
    def with_id_or_none(self, note_id: NoteId) -> VocabNote | None: return self._cache.with_id_or_none(note_id)
    def with_form(self, form: str) -> QList[VocabNote]: return self._cache.with_form(form)
    def with_compound_part(self, compound_part: str) -> QList[VocabNote]: return self._cache.with_compound_part(compound_part)
    def derived_from(self, derived_from: str) -> QList[VocabNote]: return self._cache.derived_from(derived_from)
    def with_kanji_in_main_form(self, kanji: KanjiNote) -> QList[VocabNote]: return self._cache.with_kanji_in_main_form(kanji.get_question())
    def with_kanji_in_any_form(self, kanji: KanjiNote) -> QList[VocabNote]: return self._cache.with_kanji_in_any_form(kanji.get_question())
    def with_question(self, question: str) -> QList[VocabNote]: return self._cache.with_question(question)
    def with_reading(self, question: str) -> QList[VocabNote]: return self._cache.with_reading(question)
    def with_stem(self, question: str) -> QList[VocabNote]: return self._cache.with_stem(question)

    def with_form_prefer_exact_match(self, form: str) -> QList[VocabNote]:
        matches: list[VocabNote] = self.with_form(form)
        exact_match = [voc for voc in matches if voc.question.without_noise_characters == form]
        sequence = exact_match if exact_match else matches
        return query(sequence).distinct().to_list()

    def with_any_form_in_prefer_exact_match(self, forms: list[str]) -> QList[VocabNote]:
        return query(forms).select_many(self.with_form_prefer_exact_match).distinct().to_list()  #ex_sequence.remove_duplicates_while_retaining_order(ex_sequence.flatten([self.with_form_prefer_exact_match(form) for form in forms]))

    def with_any_form_in(self, forms: list[str]) -> QList[VocabNote]:
        return query(forms).select_many(self.with_form).distinct().to_list()  #ex_sequence.remove_duplicates_while_retaining_order(ex_sequence.flatten([self.with_form(form) for form in forms]))

    def with_any_question_in(self, questions: Iterable[str]) -> QList[VocabNote]:
        return query(questions).select(self.with_question).select_many(lambda x: x).to_list()

    def add(self, note: VocabNote) -> None:
        self.collection.anki_collection.addNote(note.backend_note)
        self._cache.add_note_to_cache(note)
