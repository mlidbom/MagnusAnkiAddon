from __future__ import annotations

from typing import TYPE_CHECKING, final

from autoslot import Slots
from jaslib.note.jpnote import JPNote
from jaslib.task_runners.task_progress_runner import TaskRunner
from jastudio.anki_extentions.note_bulk_loader import NoteBulkLoader
from jastudio.note.jpnotedata_shim import JPNoteDataShim
from typed_linq_collections.collections.q_list import QList

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from anki.collection import Collection
    from anki.notes import NoteId
    from jaslib.note.jpnote_data import JPNoteData

@final
class BackEndFacade[TNote: JPNote](Slots):
    def __init__(self, anki_collection: Collection, constructor: Callable[[JPNoteData], TNote], note_type: str) -> None:
        self.anki_collection = anki_collection
        self.jp_note_constructor = constructor
        self.note_type = note_type

    def all(self) -> list[TNote]:
        with TaskRunner.current(f"Fetching all {self.note_type} notes from Anki backend") as task_runner:
            # do not use temporary variables, it will break our memory profiling using tracemalloc
            return task_runner.process_with_progress(NoteBulkLoader.load_all_notes_of_type(self.anki_collection, self.note_type),
                                                     self.jp_note_constructor, f"Constructing {self.note_type} notes")

    def search(self, query: str) -> QList[TNote]:
        return self.by_id(self.anki_collection.find_notes(query))

    def by_id(self, note_ids: Sequence[NoteId]) -> QList[TNote]:
        def note_from_id(note_id: NoteId) -> TNote:
            note = self.anki_collection.get_note(note_id)
            return self.jp_note_constructor(JPNoteDataShim.from_note(note))

        return QList(note_from_id(note_id) for note_id in note_ids)
