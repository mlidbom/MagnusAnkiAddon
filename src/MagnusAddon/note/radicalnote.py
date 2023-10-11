from __future__ import annotations

from wanikani_api import models
from anki.notes import Note

from note.waninote import WaniNote
from note.note_constants import NoteFields, Mine, NoteTypes


class RadicalNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_question(self) -> str: return self.get_field(NoteFields.Radical.question)
    def set_q(self, value: str) -> None: self.set_field(NoteFields.Radical.question, value)

    def get_answer(self) -> str: return self.get_field(NoteFields.Radical.answer)
    def set_a(self, value: str) -> None: self.set_field(NoteFields.Radical.answer, value)

    def get_meaning_mnemonic(self) -> str: return self.get_field(NoteFields.Radical.Radical_Meaning)
    def set_meaning_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Radical.Radical_Meaning, value)

    def get_radical_icon(self) -> str: return self.get_field(NoteFields.Radical.Radical_Icon)
    def set_radical_icon(self, value: str) -> None: self.set_field(NoteFields.Radical.Radical_Icon, value)

    def get_amalgamation_subject_ids(self) -> str: return self.get_field(NoteFields.Radical.amalgamation_subject_ids)
    def set_amalgamation_subject_ids(self, value: str) -> None: self.set_field(NoteFields.Radical.amalgamation_subject_ids, value)

    def update_from_wani(self, wani_radical: models.Radical) -> None:
        super().update_from_wani(wani_radical)
        self.set_meaning_mnemonic(wani_radical.meaning_mnemonic)
        self.set_a(wani_radical.meanings[0].meaning)

        amalgamation_subject_ids = [str(subject_id) for subject_id in wani_radical.amalgamation_subject_ids]
        self.set_amalgamation_subject_ids(", ".join(amalgamation_subject_ids))

    @staticmethod
    def create_from_wani_radical(wani_radical: models.Radical) -> None:
        from ankiutils import app
        note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Radical))
        note.add_tag("__imported")
        note.add_tag(Mine.Tags.Wani)
        radical_note = RadicalNote(note)
        app.anki_collection().addNote(note)
        radical_note.set_q(wani_radical.characters)
        radical_note.update_from_wani(wani_radical)

    @staticmethod
    def predicates() -> _Predicates:
        return _Predicates()



class _Predicates:
    @staticmethod
    def is_replaced_by_kanji(radical:RadicalNote) -> bool:
        return radical.get_meaning_mnemonic().upper() == "kanji"
