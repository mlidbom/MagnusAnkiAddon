from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.note_constants import NoteTypes
from note.sentences.sentencenote import SentenceNote
from typed_linq_collections.collections.q_default_dict import QDefaultDict
from typed_linq_collections.collections.q_list import QList

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner
    from note.vocabulary.vocabnote import VocabNote
    from qt_utils.task_runner_progress_dialog import ITaskRunner

class _SentenceSnapshot(CachedNote, Slots):
    def __init__(self, note: SentenceNote) -> None:
        super().__init__(note)
        self.words: tuple[str, ...] = note.get_words().to_tuple()
        self.detected_vocab: tuple[int, ...] = note.parsing_result.get().matched_vocab_ids.to_tuple()
        self.user_highlighted_vocab: tuple[str, ...] = note.configuration.highlighted_words().to_tuple()

class _SentenceCache(NoteCache[SentenceNote, _SentenceSnapshot], Slots):
    def __init__(self, all_kanji: list[SentenceNote], cache_runner: CacheRunner, task_runner: ITaskRunner) -> None:
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets
        self._by_vocab_form: QDefaultDict[str, QList[SentenceNote]] = QDefaultDict[str, QList[SentenceNote]](QList[SentenceNote])
        self._by_user_highlighted_vocab: QDefaultDict[str, QList[SentenceNote]] = QDefaultDict[str, QList[SentenceNote]](QList[SentenceNote])
        self._by_vocab_id: QDefaultDict[int, QList[SentenceNote]] = QDefaultDict[int, QList[SentenceNote]](QList[SentenceNote])
        super().__init__(all_kanji, SentenceNote, cache_runner, task_runner)

    @override
    def _create_snapshot(self, note: SentenceNote) -> _SentenceSnapshot: return _SentenceSnapshot(note)

    def with_vocab(self, vocab: VocabNote) -> QList[SentenceNote]: return self._by_vocab_id.get_value_or_default(vocab.get_id()).to_list()
    def with_vocab_form(self, form: str) -> QList[SentenceNote]: return self._by_vocab_form.get_value_or_default(form).to_list()
    def with_user_highlighted_vocab(self, form: str) -> QList[SentenceNote]: return self._by_user_highlighted_vocab.get_value_or_default(form).to_list()

    @override
    def _inheritor_remove_from_cache(self, note: SentenceNote, snapshot: _SentenceSnapshot) -> None:
        for vocab_form in snapshot.words: self._by_vocab_form[vocab_form].remove(note)
        for vocab_form in snapshot.user_highlighted_vocab: self._by_user_highlighted_vocab[vocab_form].remove(note)
        for vocab_id in snapshot.detected_vocab: self._by_vocab_id[vocab_id].remove(note)

    @override
    def _inheritor_add_to_cache(self, note: SentenceNote, snapshot: _SentenceSnapshot) -> None:
        for vocab_form in snapshot.words: self._by_vocab_form[vocab_form].append(note)
        for vocab_form in snapshot.user_highlighted_vocab: self._by_user_highlighted_vocab[vocab_form].append(note)
        for vocab_id in snapshot.detected_vocab: self._by_vocab_id[vocab_id].append(note)

class SentenceCollection(Slots):
    def __init__(self, collection: Collection, cache_manager: CacheRunner, task_runner: ITaskRunner) -> None:
        def sentence_constructor_call_while_populating_sentence_collection(note: Note) -> SentenceNote: return SentenceNote(note)
        self.collection: BackEndFacade[SentenceNote] = BackEndFacade[SentenceNote](collection, sentence_constructor_call_while_populating_sentence_collection, NoteTypes.Sentence)
        all_sentences = list(self.collection.all(task_runner))
        self._cache: _SentenceCache = _SentenceCache(all_sentences, cache_manager, task_runner)

    def all(self) -> QList[SentenceNote]: return self._cache.all()

    def with_id_or_none(self, note_id: NoteId) -> SentenceNote | None:
        return self._cache.with_id_or_none(note_id)

    def with_question(self, question: str) -> QList[SentenceNote]:
        return self._cache.with_question(question)

    def with_vocab(self, vocab_note: VocabNote) -> QList[SentenceNote]:
        matches = self._cache.with_vocab(vocab_note)
        question = vocab_note.get_question()
        # todo: isn't this check redundant, won't the match have been removed during indexing?
        return QList(match for match in matches if question not in match.configuration.incorrect_matches.words())

    def with_vocab_owned_form(self, vocab_note: VocabNote) -> QList[SentenceNote]:
        question = vocab_note.get_question()
        return (vocab_note.forms.not_owned_by_other_vocab()
                .select_many(self._cache.with_vocab_form)
                .distinct()
                .where(lambda match: question not in match.configuration.incorrect_matches.words())  # Indexing is infrequent, so this check is necessary
                .to_list())
        # owned_forms = vocab_note.forms.not_owned_by_other_vocab()
        #
        # matches = ex_sequence.remove_duplicates(ex_sequence.flatten([self._cache.with_vocab_form(form) for form in owned_forms]))
        # question = vocab_note.get_question()
        # # todo: isn't this check redundant, won't the match have been removed during indexing?
        # return [match for match in matches if question not in match.configuration.incorrect_matches.words()]

    def with_form(self, form: str) -> QList[SentenceNote]: return self._cache.with_vocab_form(form)

    def with_highlighted_vocab(self, vocab_note: VocabNote) -> QList[SentenceNote]:
        return vocab_note.forms.all_set().select_many(self._cache.with_user_highlighted_vocab).to_list()  #ex_sequence.remove_duplicates(ex_sequence.flatten([self._cache.with_user_highlighted_vocab(form) for form in vocab_note.forms.all_set()]))

    def search(self, query: str) -> QList[SentenceNote]: return self.collection.search(query)

    def add(self, note: SentenceNote) -> None:
        self.collection.anki_collection.addNote(note.backend_note)
        self._cache.add_note_to_cache(note)
