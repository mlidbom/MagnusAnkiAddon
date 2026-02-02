from __future__ import annotations

from typing import TYPE_CHECKING

from anki.models import FieldDict, NotetypeDict, NotetypeId
from anki.notes import NoteId
from jaslib.note.jpnote_data import JPNoteData
from jaslib.sysutils import typed
from jaslib.sysutils.typed import non_optional
from jastudio.qt_utils.task_progress_runner import TaskRunner

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.dbproxy import Row

class NoteBulkLoader:
    @classmethod
    def load_all_notes_of_type(cls, col: Collection, note_type_name: str) -> list[JPNoteData]:
        note_type: NotetypeDict = typed.non_optional(col.models.by_name(note_type_name))
        field_map: dict[str, tuple[int, FieldDict]] = col.models.field_map(non_optional(note_type))
        field_count = len(note_type["flds"])  # pyright: ignore[reportAny]
        note_type_id: NotetypeId = NotetypeId(note_type["id"])  # pyright: ignore[reportAny]

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

        def note_bulkloader_note_constructor(db_row: Row) -> JPNoteData:
            id: NoteId = NoteId(db_row[0]) # pyright: ignore[reportAny]
            tags: list[str] = db_row[5].split() if db_row[5] else []  # pyright: ignore[reportAny]
            field_values_list = db_row[6].split("\x1f") if db_row[6] else []  # pyright: ignore
            while len(field_values_list) < field_count: field_values_list.append("")  # pyright: ignore

            fields_dict: dict[str, str] = {}
            for name, tuple in field_map.items():
                field_index, _ = tuple
                fields_dict[name] = field_values_list[field_index]

            return JPNoteData(id, fields_dict, tags)

        with TaskRunner.current(f"Loading {note_type_name} notes from Anki db") as task_runner:
            # do not use a temporary variable for the rows, that will prevent the garbage collector from collecting them, giving us incorrect data about what takes how much memory in our tracemalloc code.
            return task_runner.process_with_progress(non_optional(col.db).all(query, note_type_id), note_bulkloader_note_constructor, f"Loading {note_type_name} notes from Anki db")
