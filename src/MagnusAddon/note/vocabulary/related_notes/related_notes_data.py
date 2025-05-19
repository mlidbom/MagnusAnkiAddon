from __future__ import annotations

from autoslot import Slots
from note.vocabulary.serialization.related_notes_serializer import VocabNoteRelatedNotesSerializer


class VocabNoteRelatedNotesData(Slots):
    serializer: VocabNoteRelatedNotesSerializer = VocabNoteRelatedNotesSerializer()
    def __init__(self, ergative_twin: str, derived_from: str, derived: set[str], similar: set[str], antonyms: set[str], confused_with: set[str]) -> None:
        self.ergative_twin: str = ergative_twin
        self.derived_from: str = derived_from

        self.derived: set[str] = derived
        self.similar: set[str] = similar
        self.antonyms: set[str] = antonyms
        self.confused_with: set[str] = confused_with
