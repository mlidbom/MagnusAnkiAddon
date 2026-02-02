from __future__ import annotations


class JPNoteData:
    def __init__(self, fields:dict[str, str], tags: list[str]) -> None:
        self.fields: dict[str, str] = fields
        self.tags: list[str] = tags