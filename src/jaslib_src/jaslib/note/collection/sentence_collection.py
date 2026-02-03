from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from typed_linq_collections.collections.q_default_dict import QDefaultDict
from typed_linq_collections.collections.q_list import QList
from typed_linq_collections.collections.q_set import QSet
from typed_linq_collections.q_iterable import query

from jaslib.note.collection.note_cache import CachedNote, NoteCache
from jaslib.note.sentences.sentencenote import SentenceNote

if TYPE_CHECKING:
    from jaslib.note.jpnote import JPNoteId
    from jaslib.note.vocabulary.vocabnote import VocabNote

class _SentenceSnapshot(CachedNote, Slots):
    def __init__(self, note: SentenceNote) -> None:
        super().__init__(note)
        self.words: tuple[str, ...] = note.get_words().to_tuple()
        self.detected_vocab: tuple[int, ...] = note.parsing_result.get().matched_vocab_ids.to_tuple()
        self.user_highlighted_vocab: tuple[str, ...] = note.configuration.highlighted_words().to_tuple()
        self.marked_incorrect_vocab: tuple[str, ...] = note.configuration.incorrect_matches.words().to_tuple()

class _SentenceCache(NoteCache[SentenceNote, _SentenceSnapshot], Slots):
    def __init__(self) -> None:
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets
        self._by_vocab_form: QDefaultDict[str, QSet[SentenceNote]] = QDefaultDict[str, QSet[SentenceNote]](QSet[SentenceNote])
        self._by_user_highlighted_vocab: QDefaultDict[str, QList[SentenceNote]] = QDefaultDict[str, QList[SentenceNote]](QList[SentenceNote])
        self._by_user_marked_invalid_vocab: QDefaultDict[str, QList[SentenceNote]] = QDefaultDict[str, QList[SentenceNote]](QList[SentenceNote])
        self._by_vocab_id: QDefaultDict[int, QSet[SentenceNote]] = QDefaultDict[int, QSet[SentenceNote]](QSet[SentenceNote])
        super().__init__(SentenceNote, SentenceNote)

    @override
    def _create_snapshot(self, note: SentenceNote) -> _SentenceSnapshot: return _SentenceSnapshot(note)

    def with_vocab(self, vocab: VocabNote) -> QList[SentenceNote]: return self._by_vocab_id.get_value_or_default(vocab.get_id()).to_list()
    def with_vocab_form(self, form: str) -> QList[SentenceNote]: return self._by_vocab_form.get_value_or_default(form).to_list()
    def with_user_highlighted_vocab(self, form: str) -> QList[SentenceNote]: return self._by_user_highlighted_vocab.get_value_or_default(form).to_list()
    def with_user_marked_invalid_vocab(self, form: str) -> QList[SentenceNote]: return self._by_user_marked_invalid_vocab.get_value_or_default(form).to_list()

    @classmethod
    def remove_first_note_with_id(cls, note_list: list[SentenceNote], id: JPNoteId) -> None:
        for index, note in enumerate(note_list):
            if note.get_id() == id:
                del note_list[index]
                return
        raise Exception(f"Could not find note with id {id} in list {note_list}")

    @override
    def _inheritor_remove_from_cache(self, note: SentenceNote, snapshot: _SentenceSnapshot) -> None:
        id = snapshot.id

        for vocab_form in snapshot.words: self._by_vocab_form[vocab_form].remove(note)
        for vocab_form in snapshot.user_highlighted_vocab: self.remove_first_note_with_id(self._by_user_highlighted_vocab[vocab_form], id)
        for vocab_form in snapshot.marked_incorrect_vocab: self.remove_first_note_with_id(self._by_user_marked_invalid_vocab[vocab_form], id)
        for vocab_id in snapshot.detected_vocab: self._by_vocab_id[vocab_id].remove(note)

    @override
    def _inheritor_add_to_cache(self, note: SentenceNote, snapshot: _SentenceSnapshot) -> None:
        for vocab_form in snapshot.words: self._by_vocab_form[vocab_form].add(note)
        for vocab_form in snapshot.user_highlighted_vocab: self._by_user_highlighted_vocab[vocab_form].append(note)
        for vocab_form in snapshot.marked_incorrect_vocab: self._by_user_marked_invalid_vocab[vocab_form].append(note)
        for vocab_id in snapshot.detected_vocab: self._by_vocab_id[vocab_id].add(note)

# noinspection PyUnusedFunction
class SentenceCollection(Slots):
    def __init__(self) -> None:
        self.cache: _SentenceCache = _SentenceCache()

    def potentially_matching_vocab(self, vocab: VocabNote) -> list[SentenceNote]:  # pyright: ignore
        if vocab.matching_configuration.requires_forbids.surface.is_required:  # noqa: SIM108
            search_strings = vocab.forms.all_list()
        else:
            search_strings = vocab.conjugator.get_stems_for_all_forms() + vocab.forms.all_list()

        questions = [it.get_question() for it in self.all()]
        matching = [it for it in questions if any(search_string in it for search_string in search_strings)]
        return (query(matching)
                .distinct()
                .select_many(self.cache.with_question)
                .distinct()
                .to_list())

    def sentences_with_substring(self, substring: str) -> list[SentenceNote]:  # pyright: ignore
        return [it for it in self.cache.all() if substring in it.get_question()]

    def all(self) -> QList[SentenceNote]: return self.cache.all()

    def with_id_or_none(self, note_id: JPNoteId) -> SentenceNote | None:
        return self.cache.with_id_or_none(note_id)

    def with_question(self, question: str) -> QList[SentenceNote]:
        return self.cache.with_question(question)

    def with_vocab(self, vocab_note: VocabNote) -> QList[SentenceNote]:
        matches = self.cache.with_vocab(vocab_note)
        question = vocab_note.get_question()
        # todo: isn't this check redundant, won't the match have been removed during indexing?
        return QList(match for match in matches if question not in match.configuration.incorrect_matches.words())

    def with_vocab_owned_form(self, vocab_note: VocabNote) -> QList[SentenceNote]:
        question = vocab_note.get_question()
        return (vocab_note.forms.not_owned_by_other_vocab()
                .select_many(self.cache.with_vocab_form)
                .distinct()
                .where(lambda match: question not in match.configuration.incorrect_matches.words())  # Indexing is infrequent, so this check is necessary
                .to_list())
        # owned_forms = vocab_note.forms.not_owned_by_other_vocab()
        #
        # matches = ex_sequence.remove_duplicates(ex_sequence.flatten([self._cache.with_vocab_form(form) for form in owned_forms]))
        # question = vocab_note.get_question()
        # # todo: isn't this check redundant, won't the match have been removed during indexing?
        # return [match for match in matches if question not in match.configuration.incorrect_matches.words()]

    def with_vocab_marked_invalid(self, vocab_note: VocabNote) -> QList[SentenceNote]:
        return self.cache.with_user_marked_invalid_vocab(vocab_note.question.disambiguation_name)

    def with_form(self, form: str) -> QList[SentenceNote]: return self.cache.with_vocab_form(form)

    def with_highlighted_vocab(self, vocab_note: VocabNote) -> QList[SentenceNote]:
        if vocab_note.question.is_disambiguated:
            return self.cache.with_user_highlighted_vocab(vocab_note.question.disambiguation_name).to_list()
        return vocab_note.forms.all_set().select_many(self.cache.with_user_highlighted_vocab).to_list()

    def add(self, note: SentenceNote) -> None:
        self.cache.add_to_cache(note)
