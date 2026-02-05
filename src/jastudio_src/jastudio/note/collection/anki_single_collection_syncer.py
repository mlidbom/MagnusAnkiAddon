from __future__ import annotations

from typing import TYPE_CHECKING

from anki.notes import NoteId
from autoslot import Slots
from JAStudio.Core.Note import JPNote
from jaspythonutils.sysutils.weak_ref import WeakRef, WeakRefable
from jastudio.ankiutils import app
from jastudio.note.jpnotedata_shim import JPNoteDataShim
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from anki.notes import Note
    from JAStudio.Core.Note import JPNoteData
    from JAStudio.Core.Note.Collection import CardStudyingStatus, NoteCacheBase
    from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner

class AnkiSingleCollectionSyncer[TNote: JPNote](WeakRefable, Slots):
    def __init__(self, all_notes: list[JPNoteData], cached_note_type: type[TNote], note_constructor: Callable[[JPNoteData], TNote], note_cache: NoteCacheBase[TNote], cache_runner: AnkiCollectionSyncRunner) -> None:
        self._note_type: type[TNote] = cached_note_type
        self._cache: NoteCacheBase[TNote] = note_cache
        self._note_constructor: Callable[[JPNoteData], TNote] = note_constructor
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets

        self._deleted: QSet[JPNoteId] = QSet()
        self._pending_add: list[Note] = []

        self._cache.init_from_list(all_notes)
        self._is_updating_anki_note: bool = False

        weakref_self = WeakRef(self)

        self._cache.on_note_updated(lambda note: weakref_self()._update_anki_note(note))

        cache_runner.connect_will_remove(lambda note_ids: weakref_self()._on_will_be_removed(note_ids))
        cache_runner.connect_note_addded(lambda note: weakref_self()._on_added(note))
        cache_runner.connect_will_flush(lambda note: weakref_self()._on_will_flush(note))

    def _update_anki_note(self, note: TNote) -> None:
        self._is_updating_anki_note = True
        try:
            if note.get_id():
                anki_note = app.anki_collection().get_note(NoteId(note.get_id()))
                JPNoteDataShim.sync_note_to_anki_note(note, anki_note)
                app.anki_collection().update_note(anki_note)
        finally:
            self._is_updating_anki_note = False

    def set_studying_statuses(self, card_statuses: list[CardStudyingStatus]) -> None:
        self._cache.set_studying_statuses(card_statuses)

    def _on_will_flush(self, backend_note: Note) -> None:
        if self._is_updating_anki_note: return
        if backend_note.id:
            cached_note = self._cache.with_id_or_none(backend_note.id)
            if cached_note is not None:
                if cached_note.is_flushing:  # our code called flush, nothing to do here
                    pass
                else:  # a note has been edited outside of our control, we need to switch to that up-to-date note and refresh generated data
                    note = self._create_note(backend_note)
                    note._unsuspended_cards = cached_note._unsuspended_cards  # pyright: ignore [reportPrivateUsage]
                    with note.recursive_flush_guard.pause_flushing():
                        note.update_generated_data()
                        self._update_anki_note(note)
                        self._cache.anki_note_updated(note)
        elif backend_note.id in self._deleted:  # undeleted note
            self._deleted.remove(backend_note.id)
            note = self._create_note(backend_note)
            with note.recursive_flush_guard.pause_flushing():
                note.update_generated_data()
                self._cache.add_to_cache(note)

    def _on_added(self, backend_note: Note) -> None:
        from jastudio.note.ankijpnote import AnkiJPNote
        note = AnkiJPNote.note_from_note(backend_note)
        if isinstance(note, self._note_type):
            self._cache.add_to_cache(note)

    def _on_will_be_removed(self, note_ids: Sequence[JPNoteId]) -> None:
        cached_notes = [it for it in (self._cache.with_id_or_none(note_id) for note_id in note_ids) if it is not None]
        self._deleted.update(it.get_id() for it in cached_notes)
        for cached in cached_notes:
            self._cache.remove_from_cache(cached)

    def _create_note(self, backend_note: Note) -> TNote:
        return self._note_constructor(JPNoteDataShim.from_note(backend_note))
