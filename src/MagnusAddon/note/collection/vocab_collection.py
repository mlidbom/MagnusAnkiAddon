from __future__ import annotations

from collections import defaultdict
from typing import Self, Sequence

from anki import hooks
from anki.collection import Collection
from anki.notes import Note, NoteId

from note.collection.backend_facade import BackEndFacade
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from note.vocabnote import VocabNote
from sysutils.lazy import Lazy

class _CachedVocab:
    def __init__(self, note: VocabNote):
        self.id = note.get_id()
        self.question = note.get_question()
        self.forms = note.get_forms()
        self.kanji = note.extract_kanji()

class _Cache:
    def __init__(self, all_vocab: list[VocabNote]):
        self._by_question: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_form: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_kanji: dict[str, set[VocabNote]] = defaultdict(set)
        self._by_id: dict[NoteId, VocabNote] = {}
        self._cached_by_id: dict[NoteId, _CachedVocab] = {}
        self._pending_add: list[VocabNote] = []

        for vocab in all_vocab:
            self._add_to_cache(vocab)

        self._setup_hooks()

    def all(self) -> list[VocabNote]: return list(self._merged_self()._by_id.values())
    def with_form(self, form: str) -> list[VocabNote]: return list(self._merged_self()._by_form[form])
    def with_kanji(self, kanji: str) -> list[VocabNote]: return list(self._merged_self()._by_kanji[kanji])

    def _merge_pending(self) -> None:
        added_vocab = [v for v in self._pending_add if v.get_id()]
        self._pending_add = [v for v in self._pending_add if not v.get_id()]
        for vocab in added_vocab:
            self._add_to_cache(vocab)

    def _merged_self(self) -> Self:
        self._merge_pending()
        return self

    def _setup_hooks(self) -> None:
        hooks.notes_will_be_deleted.append(self._on_will_be_removed)
        hooks.note_will_flush.append(self._on_will_flush)

    def _on_will_be_removed(self, _: Collection, note_ids: Sequence[NoteId]) -> None:
        cached_notes = [self._by_id[note_id] for note_id in note_ids if note_id in self._cached_by_id]
        for cached in cached_notes:
            self._remove_from_cache(cached)

    # noinspection DuplicatedCode
    def _on_will_flush(self, backend_note: Note) -> None:
        note = JPNote.note_from_note(backend_note)
        if isinstance(note, VocabNote):
            if note.get_id():
                if note.get_id() in self._by_id:
                    self._remove_from_cache(note)

                self._add_to_cache(note)
            else:
                self._pending_add.append(note)

    def _remove_from_cache(self, note: VocabNote) -> None:
        assert note.get_id()
        cached = self._cached_by_id.pop(note.get_id())
        self._by_id.pop(note.get_id())
        self._by_question[cached.question].discard(note)
        for form in cached.forms: self._by_form[form].discard(note)
        for kanji in cached.kanji: self._by_kanji[kanji].discard(note)

    def _add_to_cache(self, note: VocabNote) -> None:
        assert note.get_id()
        self._by_id[note.get_id()] = note
        self._cached_by_id[note.get_id()] = _CachedVocab(note)
        self._by_question[note.get_question()].add(note)
        for form in note.get_forms(): self._by_form[form].add(note)
        for kanji in note.extract_kanji(): self._by_kanji[kanji].add(note)

class VocabCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection
        self._cache_factory = Lazy(lambda: _Cache(self._all_internal()))

    def _cache(self) -> _Cache: return self._cache_factory.instance()

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
