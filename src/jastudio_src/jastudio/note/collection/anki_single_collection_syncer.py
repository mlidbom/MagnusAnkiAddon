from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.note.jpnote import JPNote, NoteId
from jaslib.sysutils.typed import checked_cast
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.notes import Note
    from jaslib.note.collection.note_cache import NoteCacheBase
    from jaslib.note.jpnote_data import JPNoteData
    from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner

class AnkiCachedNote(Slots):
    def __init__(self, note: JPNote) -> None:
        self.id: NoteId = note.get_id()
        self.question: str = note.get_question()

class AnkiSingleCollectionSyncer[TNote: JPNote, TSnapshot: AnkiCachedNote](Slots):
    def __init__(self, all_notes: list[JPNoteData], cached_note_type: type[TNote], note_cache: NoteCacheBase[TNote], cache_runner: AnkiCollectionSyncRunner) -> None:
        self._note_type: type[TNote] = cached_note_type
        self._cache: NoteCacheBase[TNote] = note_cache
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets

        self._by_id: dict[NoteId, TNote] = {}
        self._deleted: QSet[NoteId] = QSet()
        self._pending_add: list[Note] = []

        self._cache.init_from_list(all_notes)

        cache_runner.connect_will_remove(self._on_will_be_removed)
        cache_runner.connect_note_addded(self._on_added)
        cache_runner.connect_will_flush(self._on_will_flush)

    def _on_will_flush(self, backend_note: Note) -> None:
        if backend_note.id and backend_note.id in self._by_id:
            cached_note = self._by_id[backend_note.id]

            if cached_note.is_flushing:  # our code called flush, nothing to do here
                pass
            else:  # a note has been edited outside of our control, we need to switch to that up-to-date note and refresh generated data
                note = self._create_note(backend_note)
                with note.recursive_flush_guard.pause_flushing():
                    note.update_generated_data()
                    self._refresh_in_cache(note)
        elif backend_note.id in self._deleted:  # undeleted note
            self._deleted.remove(backend_note.id)
            note = self._create_note(backend_note)
            with note.recursive_flush_guard.pause_flushing():
                note.update_generated_data()
                self.add_note_to_cache(note)

    def _on_added(self, backend_note: Note) -> None:
        import jastudio.note.ankijpnote
        note = jastudio.note.ankijpnote.AnkiJPNote.note_from_note(backend_note)
        if isinstance(note, self._note_type):
            self.add_note_to_cache(note)

    def _on_will_be_removed(self, note_ids: Sequence[NoteId]) -> None:
        my_notes_ids = [note_id for note_id in note_ids if note_id in self._by_id]
        cached_notes = [self._by_id[note_id] for note_id in my_notes_ids]
        self._deleted.update(my_notes_ids)
        for cached in cached_notes:
            self._remove_from_cache(cached)

    def _create_note(self, backend_note: Note) -> TNote:
        import jastudio.note.ankijpnote
        return checked_cast(self._note_type, jastudio.note.ankijpnote.AnkiJPNote.note_from_note(backend_note))

    def _refresh_in_cache(self, note: TNote) -> None:
        self._remove_from_cache(note)
        self.add_note_to_cache(note)

    def _remove_from_cache(self, note: TNote) -> None:
        assert note.get_id()
        self._by_id.pop(note.get_id())

    def add_note_to_cache(self, note: TNote) -> None:
        if note.get_id() in self._by_id: return
        assert note.get_id()
        self._by_id[note.get_id()] = note
