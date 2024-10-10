from collections.abc import Callable
from typing import Sequence

from anki import hooks
from anki.collection import Collection
from anki.decks import DeckId
from anki.notes import Note, NoteId
from aqt import qconnect
from PyQt6.QtCore import QTimer

from note.note_constants import NoteTypes

class CacheRunner:
    def __init__(self, anki_collection: Collection) -> None:
        from aqt import mw
        self._pause_data_generation = False
        self._generate_data_subscribers:list[Callable[[], None]] = []
        self._merge_pending_subscribers: list[Callable[[], None]] = []
        self._will_add_subscribers: list[Callable[[Note], None]] = []
        self._will_flush_subscribers: list[Callable[[Note], None]] = []
        self._will_remove_subscribers: list[Callable[[Sequence[NoteId]], None]] = []
        self._destructors: list[Callable[[], None]] = []


        model_manager = anki_collection.models
        all_models = model_manager.all()
        our_models = [model for model in all_models if model["name"] in NoteTypes.ALL]
#        assert len(our_models) == len(NoteTypes.ALL)

        self._timer = QTimer(mw)
        qconnect(self._timer.timeout, self._on_timer)

        hooks.notes_will_be_deleted.append(self._on_will_be_removed)
        hooks.note_will_be_added.append(self._on_will_be_added)
        hooks.note_will_flush.append(self._on_will_flush)

    def start(self) -> None:
        self._timer.start(100)

    def destruct(self) -> None:
        hooks.notes_will_be_deleted.remove(self._on_will_be_removed)
        hooks.note_will_be_added.remove(self._on_will_be_added)
        hooks.note_will_flush.remove(self._on_will_flush)

        self._timer.stop()
        self._timer.disconnect()
        for destructor in self._destructors: destructor()

    def _on_timer(self) -> None:
        for subscriber in self._merge_pending_subscribers: subscriber()

        if self._pause_data_generation: return
        for callback in self._generate_data_subscribers: callback()

    def _on_will_be_added(self, _collection:Collection, backend_note: Note, _deck_id: DeckId) -> None:
        for subscriber in self._will_add_subscribers: subscriber(backend_note)

    def _on_will_flush(self, backend_note: Note) -> None:
        for subscriber in self._will_flush_subscribers: subscriber(backend_note)

    def _on_will_be_removed(self, _: Collection, note_ids: Sequence[NoteId]) -> None:
        for subscriber in self._will_remove_subscribers: subscriber(note_ids)


    def pause_data_generation(self) -> None:
        self._pause_data_generation = True

    def resume_data_generation(self) -> None:
        self._pause_data_generation = False

    def connect_generate_data_timer(self, flush_updates: Callable[[], None]) -> None:
        self._generate_data_subscribers.append(flush_updates)

    def connect_destruct(self, destruct: Callable[[], None]) -> None:
        self._destructors.append(destruct)

    def connect_merge_pending_adds(self, _merge_pending_added_notes:Callable[[], None]) -> None:
        self._merge_pending_subscribers.append(_merge_pending_added_notes)

    def connect_will_add(self, _merge_pending_added_notes: Callable[[Note], None]) -> None:
        self._will_add_subscribers.append(_merge_pending_added_notes)

    def connect_will_flush(self, _merge_pending_added_notes: Callable[[Note], None]) -> None:
        self._will_flush_subscribers.append(_merge_pending_added_notes)

    def connect_will_remove(self, _merge_pending_added_notes: Callable[[Sequence[NoteId]], None]) -> None:
        self._will_remove_subscribers.append(_merge_pending_added_notes)

    def _check_for_updated_note_types(self) -> None:
        from ankiutils import app

        def schema_matches(own_schema, other_schema) -> bool:
            if len(own_schema) != len(other_schema): return False
            for key, value in own_schema.items():
                if key not in other_schema:
                    return False

                own_index = value[0]
                other_index = other_schema[key][0]

                if own_index != other_index: return False

            return True

        for cached_note_type in self._note_types:
            current_note_type = [nt for nt in app.anki_collection().models.all() if nt["name"] == cached_note_type["name"]][0]
            assert schema_matches(cached_note_type["flds"], current_note_type["flds"])




