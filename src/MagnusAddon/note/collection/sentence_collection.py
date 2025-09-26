from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, override

from ex_autoslot import AutoSlots
from line_profiling_hacks import profile_lines
from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.note_constants import NoteTypes
from note.sentences.sentencenote import SentenceNote

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner
    from note.vocabulary.vocabnote import VocabNote
    from qt_utils.task_runner_progress_dialog import ITaskRunner
    from typed_linq_collections.collections.q_list import QList

class _SentenceSnapshot(CachedNote, AutoSlots):
    @profile_lines
    def __init__(self, note: SentenceNote) -> None:
        super().__init__(note)
        self.words: set[str] = note.get_words()
        self.detected_vocab: set[int] = note.parsing_result.get().matched_vocab_ids
        self.user_highlighted_vocab: set[str] = set(note.configuration.highlighted_words())

class _SentenceCache(NoteCache[SentenceNote, _SentenceSnapshot], AutoSlots):
    @profile_lines
    def __init__(self, all_kanji: list[SentenceNote], cache_runner: CacheRunner, task_runner: ITaskRunner) -> None:
        self._by_vocab_form: dict[str, set[SentenceNote]] = defaultdict(set)
        self._by_user_highlighted_vocab: dict[str, set[SentenceNote]] = defaultdict(set)
        self._by_vocab_id: dict[int, set[SentenceNote]] = defaultdict(set)
        super().__init__(all_kanji, SentenceNote, cache_runner, task_runner)

    @override
    def _create_snapshot(self, note: SentenceNote) -> _SentenceSnapshot: return _SentenceSnapshot(note)

    def with_vocab(self, vocab: VocabNote) -> list[SentenceNote]: return list(self._by_vocab_id[vocab.get_id()])
    def with_vocab_form(self, form: str) -> list[SentenceNote]: return list(self._by_vocab_form[form])
    def with_user_highlighted_vocab(self, form: str) -> list[SentenceNote]: return list(self._by_user_highlighted_vocab[form])

    @override
    def _inheritor_remove_from_cache(self, note: SentenceNote, snapshot: _SentenceSnapshot) -> None:
        for vocab_form in snapshot.words: self._by_vocab_form[vocab_form].remove(note)
        for vocab_form in snapshot.user_highlighted_vocab: self._by_user_highlighted_vocab[vocab_form].remove(note)
        for vocab_id in snapshot.detected_vocab: self._by_vocab_id[vocab_id].remove(note)

    @override
    def _inheritor_add_to_cache(self, note: SentenceNote, snapshot: _SentenceSnapshot) -> None:
        for vocab_form in snapshot.words: self._by_vocab_form[vocab_form].add(note)
        for vocab_form in snapshot.user_highlighted_vocab: self._by_user_highlighted_vocab[vocab_form].add(note)
        for vocab_id in snapshot.detected_vocab: self._by_vocab_id[vocab_id].add(note)

class SentenceCollection(AutoSlots):
    @profile_lines
    def __init__(self, collection: Collection, cache_manager: CacheRunner, task_runner: ITaskRunner) -> None:
        def sentence_constructor_call_while_populating_sentence_collection(note: Note) -> SentenceNote: return SentenceNote(note)
        self.collection: BackEndFacade[SentenceNote] = BackEndFacade[SentenceNote](collection, sentence_constructor_call_while_populating_sentence_collection, NoteTypes.Sentence)
        all_sentences = list(self.collection.all(task_runner))
        self._cache: _SentenceCache = _SentenceCache(all_sentences, cache_manager, task_runner)

    def all(self) -> list[SentenceNote]: return self._cache.all()

    def with_id_or_none(self, note_id: NoteId) -> SentenceNote | None:
        return self._cache.with_id_or_none(note_id)

    def with_question(self, question: str) -> QList[SentenceNote]:
        return self._cache.with_question(question)

    def with_vocab(self, vocab_note: VocabNote) -> list[SentenceNote]:
        matches = self._cache.with_vocab(vocab_note)
        question = vocab_note.get_question()
        # todo: isn't this check redundant, won't the match have been removed during indexing?
        return [match for match in matches if question not in match.configuration.incorrect_matches.words()]

    def with_vocab_owned_form(self, vocab_note: VocabNote) -> QList[SentenceNote]:
        question = vocab_note.get_question()
        return (vocab_note.forms.not_owned_by_other_vocab()
                .select_many(self._cache.with_vocab_form)
                .distinct()
                .where(lambda match: question not in match.configuration.incorrect_matches.words())  # todo: isn't this check redundant, won't the match have been removed during indexing?
                .to_list())
        # owned_forms = vocab_note.forms.not_owned_by_other_vocab()
        #
        # matches = ex_sequence.remove_duplicates(ex_sequence.flatten([self._cache.with_vocab_form(form) for form in owned_forms]))
        # question = vocab_note.get_question()
        # # todo: isn't this check redundant, won't the match have been removed during indexing?
        # return [match for match in matches if question not in match.configuration.incorrect_matches.words()]

    def with_form(self, form: str) -> list[SentenceNote]: return self._cache.with_vocab_form(form)

    def with_highlighted_vocab(self, vocab_note: VocabNote) -> QList[SentenceNote]:
        return vocab_note.forms.all_set().select_many(self._cache.with_user_highlighted_vocab).to_list()  #ex_sequence.remove_duplicates(ex_sequence.flatten([self._cache.with_user_highlighted_vocab(form) for form in vocab_note.forms.all_set()]))

    def search(self, query: str) -> list[SentenceNote]: return list(self.collection.search(query))

    def add(self, note: SentenceNote) -> None:
        self.collection.anki_collection.addNote(note.backend_note)
        self._cache.add_note_to_cache(note)
