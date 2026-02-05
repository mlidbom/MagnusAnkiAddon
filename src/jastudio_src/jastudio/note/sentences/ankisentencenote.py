from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from JAStudio.Core.Note import ImmersionKitSentenceNoteFields, SentenceNote, Tags
from jastudio.note.ankijpnote import AnkiJPNote
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from anki.notes import Note

class AnkiSentenceNote(AnkiJPNote, Slots):
    @classmethod
    def import_immersion_kit_sentence(cls, immersion_kit_note: Note) -> SentenceNote:
        created = SentenceNote.AddSentence(question=immersion_kit_note[ImmersionKitSentenceNoteFields.Question],
                                            answer=immersion_kit_note[ImmersionKitSentenceNoteFields.Answer],
                                            audio=immersion_kit_note[ImmersionKitSentenceNoteFields.Audio],
                                            screenshot=immersion_kit_note[ImmersionKitSentenceNoteFields.Screenshot],
                                            tags=QSet([Tags.Source.ImmersionKit]))

        created.Id.Set(immersion_kit_note[ImmersionKitSentenceNoteFields.Id])
        created.Reading.Set(immersion_kit_note[ImmersionKitSentenceNoteFields.Reading])

        return created