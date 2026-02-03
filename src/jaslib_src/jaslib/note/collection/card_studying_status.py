from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anki.notes import NoteId


class CardStudyingStatus:
    def __init__(self, note_id: NoteId, card_type: str, is_suspended: bool, note_type_name: str) -> None:
        self.note_id: NoteId = note_id
        self.card_type: str = card_type
        self.is_suspended: bool = is_suspended
        self.note_type_name: str = note_type_name