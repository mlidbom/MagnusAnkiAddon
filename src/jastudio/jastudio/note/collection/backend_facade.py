from __future__ import annotations

from typing import TYPE_CHECKING, final

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.note.jpnote import JPNote
from qt_utils.task_progress_runner import TaskRunner
from typed_linq_collections.collections.q_list import QList

from jastudio.anki_extentions.note_ex import NoteBulkLoader

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from anki.collection import Collection
    from anki.notes import Note, NoteId

@final
class BackEndFacade[TNote: JPNote](Slots):
    def __init__(self, anki_collection: Collection, constructor: Callable[[Note], TNote], note_type: str) -> None:
        self.anki_collection = anki_collection
        self.jp_note_constructor = constructor
        self.note_type = note_type

    def all(self) -> list[TNote]:
        with TaskRunner.current(f"Fetching all {self.note_type} notes from Anki backend") as task_runner:
            #do not use temporary variables, it will break our memory profiling using tracemalloc
            return task_runner.process_with_progress(NoteBulkLoader.load_all_notes_of_type(self.anki_collection, self.note_type),
                                                     self.jp_note_constructor, f"Constructing {self.note_type} notes")

    def search(self, query: str) -> QList[TNote]:
        return self.by_id(self.anki_collection.find_notes(query))

    def by_id(self, note_ids: Sequence[NoteId]) -> QList[TNote]:
        return QList(self.jp_note_constructor(self.anki_collection.get_note(note_id)) for note_id in note_ids)
