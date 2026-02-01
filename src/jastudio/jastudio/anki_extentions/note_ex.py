from __future__ import annotations

from typing import TYPE_CHECKING

from anki.models import FieldDict, NotetypeDict, NotetypeId
from anki.notes import Note, NoteId
from jastudio.qt_utils.task_progress_runner import TaskRunner
from sysutils import typed
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.dbproxy import Row

class NoteBulkLoader:
    @classmethod
    def load_all_notes_of_type(cls, col: Collection, note_type_name: str) -> list[Note]:
        note_type: NotetypeDict = typed.non_optional(col.models.by_name(note_type_name))
        field_map: dict[str, tuple[int, FieldDict]] = col.models.field_map(non_optional(note_type))
        field_count = len(note_type["flds"]) # pyright: ignore[reportAny]
        note_type_id: NotetypeId = NotetypeId(note_type["id"]) # pyright: ignore[reportAny]
        col_weak_ref: Collection = col.weakref()

        query = """
                SELECT notes.id,  -- 0
                       notes.guid,-- 1
                       notes.mid, -- 2
                       notes.mod, -- 3
                       notes.usn, -- 4
                       notes.tags,-- 5
                       notes.flds -- 6
                from notes
                WHERE notes.mid = ?
                """

        def note_bulkloader_note_constructor(row: Row) -> Note:
            return NoteBulkLoader._NoteEx(col_weak_ref, row, field_map, field_count)

        with TaskRunner.current(f"Loading {note_type_name} notes from Anki db") as task_runner:
            #do not use a temporary variable for the rows, that will prevent the garbage collector from collecting them, giving us incorrect data about what takes how much memory in our tracemalloc code.
            return task_runner.process_with_progress(non_optional(col.db).all(query, note_type_id), note_bulkloader_note_constructor, f"Loading {note_type_name} notes from Anki db")

    # noinspection PyMissingConstructor
    class _NoteEx(Note):
        # noinspection PyMissingConstructor this is very much intentional. We do NOT want the base class to go fetching the note's data from the db. Avoiding that is the whole point of this class and improves performance tenfold or more.
        def __init__(self, collection_weak_ref: Collection, db_row: Row, field_map: dict[str, tuple[int, FieldDict]], field_count: int) -> None: # pyright: ignore[reportMissingSuperCall]
            self.col: Collection = collection_weak_ref
            self.id: NoteId = NoteId(db_row[0]) # pyright: ignore[reportAny]
            self.guid: str = db_row[1]
            self.mid: NotetypeId = NotetypeId(db_row[2]) # pyright: ignore[reportAny]
            self.mod: int = db_row[3]
            self.usn: int = db_row[4]
            self.tags: list[str] = db_row[5].split() if db_row[5] else [] # pyright: ignore[reportAny]

            field_values = db_row[6].split("\x1f") if db_row[6] else [] # pyright: ignore
            while len(field_values) < field_count: field_values.append("") # pyright: ignore
            self.fields:list[str] = field_values
            self._fmap:dict[str, tuple[int, FieldDict]] = field_map
