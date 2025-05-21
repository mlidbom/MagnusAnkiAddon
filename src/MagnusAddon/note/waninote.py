from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.jpnote import JPNote

if TYPE_CHECKING:
    from anki.notes import Note
    from wanikani_api import models


class WaniNote(JPNote, Slots):
    def __init__(self, note: Note) -> None:
        super().__init__(note)


    def update_from_wani(self, wani_model: models.Subject) -> None:
        pass
