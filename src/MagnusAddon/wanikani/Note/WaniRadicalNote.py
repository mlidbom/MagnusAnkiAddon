from _lib.wanikani_api import models
from anki.notes import Note
from aqt import mw

from wanikani.Note.WaniNote import WaniNote
from wanikani.wani_constants import Wani, Mine


class WaniRadicalNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_radical_name(self): return super().get_field(Wani.RadicalFields.Radical_Name)
    def set_radical_name(self, value: str) -> None: super().set_field(Wani.RadicalFields.Radical_Name, value)

    def get_radical(self): return super().get_field(Wani.RadicalFields.Radical)
    def set_radical(self, value: str) -> None: super().set_field(Wani.RadicalFields.Radical, value)

    def get_meaning_mnemonic(self): return super().get_field(Wani.RadicalFields.Radical_Meaning)
    def set_meaning_mnemonic(self, value: str) -> None: super().set_field(Wani.RadicalFields.Radical_Meaning, value)

    def get_radical_icon(self): return super().get_field(Wani.RadicalFields.Radical_Icon)
    def set_radical_icon(self, value: str) -> None: super().set_field(Wani.RadicalFields.Radical_Icon, value)

    def get_amalgamation_subject_ids(self): return super().get_field(Wani.RadicalFields.amalgamation_subject_ids)
    def set_amalgamation_subject_ids(self, value: str) -> None: super().set_field(Wani.RadicalFields.amalgamation_subject_ids, value)

    def update_from_wani(self, wani_radical: models.Radical):
        super().update_from_wani(wani_radical)
        self.set_meaning_mnemonic(wani_radical.meaning_mnemonic)
        self.set_radical_name(wani_radical.meanings[0].meaning)

        amalgamation_subject_ids = [str(id) for id in wani_radical.amalgamation_subject_ids]
        self.set_amalgamation_subject_ids(", ".join(amalgamation_subject_ids))

        self.set_level(wani_radical.level)

    def create_from_wani_radical(wani_radical: models.Radical):
        note = Note(mw.col, mw.col.models.byName(Wani.NoteType.Radical))
        note.add_tag("__imported")
        note.add_tag(Mine.Tags.Wani)
        radical_note = WaniRadicalNote(note)
        mw.col.addNote(note)
        radical_note.set_radical(wani_radical.characters)
        radical_note.update_from_wani(wani_radical)
