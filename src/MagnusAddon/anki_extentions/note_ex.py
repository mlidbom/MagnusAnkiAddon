from __future__ import annotations

from typing import TYPE_CHECKING

from anki.models import FieldDict, NotetypeDict, NotetypeId
from anki.notes import Note, NoteId
from sysutils import typed
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.dbproxy import Row
    from qt_utils.task_runner_progress_dialog import ITaskRunner

class NoteBulkLoader:
    @staticmethod
    def load_all_notes_of_type(col: Collection, note_type_name: str, task_runner: ITaskRunner) -> list[Note]:
        note_type: NotetypeDict = typed.non_optional(col.models.by_name(note_type_name))
        field_map: dict[str, tuple[int, FieldDict]] = col.models.field_map(non_optional(note_type))
        field_count = len(note_type["flds"])
        col_weak_ref = col.weakref()

        query = """
                SELECT notes.id,  -- 0
                       notes.guid,-- 1
                       notes.mid, -- 2
                       notes.mod, -- 3
                       notes.usn, -- 4
                       notes.tags,-- 5
                       notes.flds -- 6
                FROM notes
                         JOIN notetypes ON notes.mid = notetypes.id
                WHERE notetypes.name COLLATE NOCASE = ?
                """

        rows = non_optional(col.db).all(query, note_type_name)

        def note_bulkloader_note_constructor(row: Row) -> Note:
            return NoteBulkLoader._NoteEx(col_weak_ref, row, field_map, field_count)

        return task_runner.process_with_progress(rows, note_bulkloader_note_constructor, f"Loading {note_type_name} notes from Anki db")

    class _NoteEx(Note):
        def __init__(self, collection_weak_ref: Collection, db_row: Row, field_map: dict[str, tuple[int, FieldDict]], field_count: int) -> None:
            self.col = collection_weak_ref
            self.id = NoteId(db_row[0])
            self.guid = db_row[1]
            self.mid = NotetypeId(db_row[2])
            self.mod = db_row[3]
            self.usn = db_row[4]
            self.tags = db_row[5].split() if db_row[5] else []

            field_values = db_row[6].split("\x1f") if db_row[6] else []
            while len(field_values) < field_count: field_values.append("")
            self.fields = field_values
            self._fmap = field_map
