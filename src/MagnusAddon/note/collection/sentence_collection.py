from __future__ import annotations

from anki.collection import Collection
from anki.notes import Note, NoteId
from collections import defaultdict

from note.collection.backend_facade import BackEndFacade
from note.collection.cache_runner import CacheRunner
from note.collection.note_cache import CachedNote, NoteCache
from note.note_constants import NoteTypes
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_sequence

class _SentenceSnapshot(CachedNote):
    def __init__(self, note: SentenceNote):
        super().__init__(note)
        self.words = note.get_words()
        self.user_highlighted_vocab = set(note.get_user_highlighted_vocab())

class _SentenceCache(NoteCache[SentenceNote, _SentenceSnapshot]):
    def __init__(self, all_kanji: list[SentenceNote], cache_runner: CacheRunner):
        self._by_vocab_form: dict[str, set[SentenceNote]] = defaultdict(set)
        self._by_user_highlighted_vocab: dict[str, set[SentenceNote]] = defaultdict(set)
        super().__init__(all_kanji, SentenceNote, cache_runner)

    def _create_snapshot(self, note: SentenceNote) -> _SentenceSnapshot: return _SentenceSnapshot(note)

    def with_vocab_form(self, form: str) -> list[SentenceNote]: return list(self._by_vocab_form[form])
    def with_user_highlighted_vocab(self, form: str) -> list[SentenceNote]: return list(self._by_user_highlighted_vocab[form])

    def _inheritor_remove_from_cache(self, sentence: SentenceNote, cached:_SentenceSnapshot) -> None:
        for vocab_form in cached.words: self._by_vocab_form[vocab_form].remove(sentence)
        for vocab_form in cached.user_highlighted_vocab: self._by_user_highlighted_vocab[vocab_form].remove(sentence)

    def _inheritor_add_to_cache(self, sentence: SentenceNote) -> None:
        for vocab_form in sentence.get_words(): self._by_vocab_form[vocab_form].add(sentence)
        for vocab_form in sentence.get_user_highlighted_vocab(): self._by_user_highlighted_vocab[vocab_form].add(sentence)


class SentenceCollection:
    def __init__(self, collection: Collection, cache_manager: CacheRunner):
        def sentence_constructor(note: Note) -> SentenceNote: return SentenceNote(note)
        self.collection = BackEndFacade[SentenceNote](collection, sentence_constructor, NoteTypes.Sentence)
        self._cache = _SentenceCache(list(self.collection.all()), cache_manager)

    def all(self) -> list[SentenceNote]: return self._cache.all()

    def with_id(self, note_id:NoteId) -> SentenceNote:
        return self._cache.with_id(note_id)

    def with_question(self, question: str) -> list[SentenceNote]:
        return self._cache.with_question(question)

    def with_vocab(self, vocab_note: VocabNote) -> list[SentenceNote]:
        matches = ex_sequence.remove_duplicates(ex_sequence.flatten([self._cache.with_vocab_form(form) for form in vocab_note.get_forms()]))
        question = vocab_note.get_question()
        return [match for match in matches if question not in match.get_user_excluded_vocab()]

    def with_form(self, form:str) -> list[SentenceNote]: return self._cache.with_vocab_form(form)

    def with_highlighted_vocab(self, vocab_note: VocabNote) -> list[SentenceNote]:
        return ex_sequence.remove_duplicates(ex_sequence.flatten([self._cache.with_user_highlighted_vocab(form) for form in vocab_note.get_forms()]))

    def search(self, query: str) -> list[SentenceNote]: return list(self.collection.search(query))
