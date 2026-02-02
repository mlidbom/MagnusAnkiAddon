from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.note.note_constants import ImmersionKitSentenceNoteFields
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib.note.tags import Tags
from jastudio.note.ankijpnote import AnkiJPNote
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from anki.notes import Note

class AnkiSentenceNote(AnkiJPNote, Slots):
    @classmethod
    def import_immersion_kit_sentence(cls, immersion_kit_note: Note) -> SentenceNote:
        created = SentenceNote.add_sentence(question=immersion_kit_note[ImmersionKitSentenceNoteFields.question],
                                            answer=immersion_kit_note[ImmersionKitSentenceNoteFields.answer],
                                            audio=immersion_kit_note[ImmersionKitSentenceNoteFields.audio],
                                            screenshot=immersion_kit_note[ImmersionKitSentenceNoteFields.screenshot],
                                            tags=QSet([Tags.Source.immersion_kit]))

        created.id.set(immersion_kit_note[ImmersionKitSentenceNoteFields.id])
        created.reading.set(immersion_kit_note[ImmersionKitSentenceNoteFields.reading])

        return created