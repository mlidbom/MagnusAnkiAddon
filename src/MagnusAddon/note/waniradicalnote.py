from wanikani_api import models
from anki.notes import Note

from ankiutils.anki_shim import facade
from note.waninote import WaniNote
from wanikani.wani_constants import Wani, Mine


class WaniRadicalNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_q(self) -> str: return super().get_field(Wani.RadicalFields.question)
    def set_q(self, value: str) -> None: super().set_field(Wani.RadicalFields.question, value)

    def get_a(self) -> str: return super().get_field(Wani.RadicalFields.answer)
    def set_a(self, value: str) -> None: super().set_field(Wani.RadicalFields.answer, value)

    def get_meaning_mnemonic(self) -> str: return super().get_field(Wani.RadicalFields.Radical_Meaning)
    def set_meaning_mnemonic(self, value: str) -> None: super().set_field(Wani.RadicalFields.Radical_Meaning, value)

    def get_radical_icon(self) -> str: return super().get_field(Wani.RadicalFields.Radical_Icon)
    def set_radical_icon(self, value: str) -> None: super().set_field(Wani.RadicalFields.Radical_Icon, value)

    def get_amalgamation_subject_ids(self) -> str: return super().get_field(Wani.RadicalFields.amalgamation_subject_ids)
    def set_amalgamation_subject_ids(self, value: str) -> None: super().set_field(Wani.RadicalFields.amalgamation_subject_ids, value)

    def update_from_wani(self, wani_radical: models.Radical):
        super().update_from_wani(wani_radical)
        self.set_meaning_mnemonic(wani_radical.meaning_mnemonic)
        self.set_a(wani_radical.meanings[0].meaning)

        amalgamation_subject_ids = [str(subject_id) for subject_id in wani_radical.amalgamation_subject_ids]
        self.set_amalgamation_subject_ids(", ".join(amalgamation_subject_ids))

        self.set_level(wani_radical.level)

    @staticmethod
    def create_from_wani_radical(wani_radical: models.Radical):
        note = Note(facade.col(), facade.col().models.byName(Wani.NoteType.Radical))
        note.add_tag("__imported")
        note.add_tag(Mine.Tags.Wani)
        radical_note = WaniRadicalNote(note)
        facade.col().addNote(note)
        radical_note.set_q(wani_radical.characters)
        radical_note.update_from_wani(wani_radical)
