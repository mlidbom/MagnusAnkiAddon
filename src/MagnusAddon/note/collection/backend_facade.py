from __future__ import annotations

from typing import TYPE_CHECKING, final

from anki_extentions.note_ex import NoteBulkLoader
from ex_autoslot import AutoSlots
from line_profiling_hacks import profile_lines
from note.jpnote import JPNote

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from anki.collection import Collection
    from anki.notes import Note, NoteId
    from qt_utils.task_runner_progress_dialog import ITaskRunner

@final
class BackEndFacade[TNote: JPNote](AutoSlots):
    def __init__(self, anki_collection: Collection, constructor: Callable[[Note], TNote], note_type: str) -> None:
        self.anki_collection = anki_collection
        self.jp_note_constructor = constructor
        self.note_type = note_type

    @profile_lines
    def all(self, task_runner: ITaskRunner) -> list[TNote]:
        backend_notes = NoteBulkLoader.load_all_notes_of_type(self.anki_collection, self.note_type, task_runner)
        return task_runner.process_with_progress(backend_notes, self.jp_note_constructor, f"Constructing {self.note_type} notes")

    def search(self, query: str) -> list[TNote]:
        return self.by_id(self.anki_collection.find_notes(query))

    def by_id(self, note_ids: Sequence[NoteId]) -> list[TNote]:
        return [self.jp_note_constructor(self.anki_collection.get_note(note_id)) for note_id in note_ids]
