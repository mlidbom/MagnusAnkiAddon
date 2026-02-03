from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jaslib.note.jpnote import JPNoteId


class JPNoteData:
    def __init__(self, id: JPNoteId, fields:dict[str, str], tags: list[str]) -> None:
        self.id: JPNoteId = id
        self.fields: dict[str, str] = fields
        self.tags: list[str] = tags