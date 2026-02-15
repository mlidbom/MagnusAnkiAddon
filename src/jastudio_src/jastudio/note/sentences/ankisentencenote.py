from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jastudio.note.ankijpnote import AnkiJPNote

if TYPE_CHECKING:
    from anki.notes import Note
    from JAStudio.Core.Note.Sentences import SentenceNote

class AnkiSentenceNote(AnkiJPNote, Slots):
    @classmethod
    def import_immersion_kit_sentence(cls, immersion_kit_note: Note) -> SentenceNote:  # pyright: ignore
        raise NotImplementedError()
        #todo migration
        # created = SentenceNote.AddSentence(dotnet_ui_root.Services.NoteServices,
        #                                    question=immersion_kit_note[ImmersionKitSentenceNoteFields.question],
        #                                    answer=immersion_kit_note[ImmersionKitSentenceNoteFields.answer],
        #                                    audio=immersion_kit_note[ImmersionKitSentenceNoteFields.audio],
        #                                    screenshot=immersion_kit_note[ImmersionKitSentenceNoteFields.screenshot],
        #                                    tags=QSet([Tags.Source.ImmersionKit]))
        #
        # created.id.set(immersion_kit_note[ImmersionKitSentenceNoteFields.id])
        # created.reading.set(immersion_kit_note[ImmersionKitSentenceNoteFields.reading])
        #
        # return created
