from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jaslib.note.jpnote import NoteId


class JPNoteData:
    def __init__(self, id: NoteId, fields:dict[str, str], tags: list[str]) -> None:
        self.id: NoteId = id
        self.fields: dict[str, str] = fields
        self.tags: list[str] = tags