from __future__ import annotations

from typing import TYPE_CHECKING, final

from autoslot import Slots
from note.jpnote import JPNote
from note.note_constants import Builtin

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from anki.collection import Collection
    from anki.notes import Note, NoteId
    from qt_utils.task_runner_progress_dialog import ITaskRunner

@final
class BackEndFacade[TNote: JPNote](Slots):
    def __init__(self, anki_collection: Collection, constructor: Callable[[Note], TNote], note_type: str) -> None:
        self.anki_collection = anki_collection
        self.constructor = constructor
        self.note_type = note_type

    def all(self, task_runner: ITaskRunner, note_type: str) -> list[TNote]:
        task_runner.set_label_text(f"Listing {note_type} notes from Anki db")
        note_ids = list(self.anki_collection.find_notes(f"{Builtin.Note}:{self.note_type}"))
        backend_notes = task_runner.process_with_progress(note_ids, self.anki_collection.get_note, f"Loading {self.note_type} notes from Anki db")
        jp_notes = task_runner.process_with_progress(backend_notes, self.constructor, f"Constructing {self.note_type} notes")
        return jp_notes  # noqa: RET504

    # noinspection PySameParameterValue
    def search(self, query: str) -> list[TNote]:
        return self.by_id(self.anki_collection.find_notes(query))

    def by_id(self, note_ids: Sequence[NoteId]) -> list[TNote]:
        return [self.constructor(self.anki_collection.get_note(note_id)) for note_id in note_ids]
