from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.note.collection.card_studying_status import CardStudyingStatus
from jaslib.note.jpnote import JPNote, JPNoteId
from jastudio.note.jpnotedata_shim import JPNoteDataShim
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from anki.notes import Note
    from jaslib.note.collection.note_cache import NoteCacheBase
    from jaslib.note.jpnote_data import JPNoteData
    from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner

class AnkiSingleCollectionSyncer[TNote: JPNote](Slots):
    def __init__(self, all_notes: list[JPNoteData], cached_note_type: type[TNote], note_constructor: Callable[[JPNoteData], TNote], note_cache: NoteCacheBase[TNote], cache_runner: AnkiCollectionSyncRunner) -> None:
        self._note_type: type[TNote] = cached_note_type
        self._cache: NoteCacheBase[TNote] = note_cache
        self._note_constructor: Callable[[JPNoteData], TNote] = note_constructor
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets

        self._deleted: QSet[JPNoteId] = QSet()
        self._pending_add: list[Note] = []

        self._cache.init_from_list(all_notes)

        cache_runner.connect_will_remove(self._on_will_be_removed)
        cache_runner.connect_note_addded(self._on_added)
        cache_runner.connect_will_flush(self._on_will_flush)

    def set_studying_statuses(self, card_statuses: list[CardStudyingStatus]) -> None:
        self._cache.set_studying_statuses(card_statuses)

    def _on_will_flush(self, backend_note: Note) -> None:
        if backend_note.id:
            cached_note = self._cache.with_id_or_none(backend_note.id)
            if cached_note is not None:
                if cached_note.is_flushing:  # our code called flush, nothing to do here
                    pass
                else:  # a note has been edited outside of our control, we need to switch to that up-to-date note and refresh generated data
                    note = self._create_note(backend_note)
                    with note.recursive_flush_guard.pause_flushing():
                        note.update_generated_data()
                        self._cache.refresh_in_cache(note)
        elif backend_note.id in self._deleted:  # undeleted note
            self._deleted.remove(backend_note.id)
            note = self._create_note(backend_note)
            with note.recursive_flush_guard.pause_flushing():
                note.update_generated_data()
                self._cache.add_to_cache(note)

    def _on_added(self, backend_note: Note) -> None:
        import jastudio.note.ankijpnote
        note = jastudio.note.ankijpnote.AnkiJPNote.note_from_note(backend_note)
        if isinstance(note, self._note_type):
            self._cache.add_to_cache(note)

    def _on_will_be_removed(self, note_ids: Sequence[JPNoteId]) -> None:
        cached_notes = [it for it in (self._cache.with_id_or_none(note_id) for note_id in note_ids) if it is not None]
        self._deleted.update(it.get_id() for it in cached_notes)
        for cached in cached_notes:
            self._cache.remove_from_cache(cached)

    def _create_note(self, backend_note: Note) -> TNote:
        return self._note_constructor(JPNoteDataShim.from_note(backend_note))
