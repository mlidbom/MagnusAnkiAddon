from typing import Sequence

from wanikani_api import models
from anki.notes import Note

from ankiutils.anki_shim import facade
from note.jpnote import JPNote
from note.note_constants import Mine, NoteFields


class WaniNote(JPNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_level_tag(self) -> int:
        level_tag = [level for level in self._note.tags if level.startswith('level')][0]
        level_int = int(level_tag[5:])
        return level_int

    def set_level_tag(self, new_level: int) -> None:
        level_tags = [level for level in self._note.tags if level.startswith('level')]
        for level in level_tags:
            self._note.remove_tag(level)
        self._note.add_tag("level{:02d}".format(new_level))
        self._note.flush()

    def get_sort_id(self) -> str: return self.get_field(NoteFields.NoteFields.sort_id)
    def set_sort_id(self, value: str) -> None: self.set_field(NoteFields.NoteFields.sort_id, value)

    def get_subject_id(self) -> int: return int(self.get_field(NoteFields.NoteFields.subject_id))
    def set_subject_id(self, value: int) -> None: self.set_field(NoteFields.NoteFields.subject_id, str(value))

    def get_lesson_position(self) -> int:
        if not self.is_wani_note(): return 0
        return int(self.get_field(NoteFields.NoteFields.lesson_position))

    def set_lesson_position(self, value: int) -> None:
        current_position = self.get_field(NoteFields.NoteFields.lesson_position)

        # Wani api does some weird stuff sometimes returning 0 as lesson positions for many subjects.
        # Possibly the ones in the current level or currently being studied.
        # Anyway, we do NOT want to overwrite valid lesson positions with zeroes!
        if value > 0:
            self.set_field(NoteFields.NoteFields.lesson_position, str(value))
        else:
            if current_position == "0" or current_position == "" or current_position is None:
                self.set_field(NoteFields.NoteFields.lesson_position, str(value))
            else:
                print("Ignoring 0 as value for lesson_position for subject: {}".format(self.get_subject_id()))


    def get_my_learning_order(self) -> str: return self.get_field(NoteFields.NoteFields.my_learning_order)
    def _set_my_learning_order(self, value: str) -> None: self.set_field(NoteFields.NoteFields.my_learning_order, value)

    def get_document_url(self) -> str: return self.get_field(NoteFields.NoteFields.document_url)
    def set_document_url(self, value: str) -> None: self.set_field(NoteFields.NoteFields.document_url, value)

    def get_level(self) -> int:
        if not self.is_wani_note():
            return 0 #non wani items
        return int(self.get_field(NoteFields.NoteFields.level))

    def set_level(self, value: int) -> None:
        self.set_level_tag(value)
        self.set_field(NoteFields.NoteFields.level, str(value))

    def set_auxiliary_meanings_whitelist(self, value:str) -> None: self.set_field(NoteFields.NoteFields.auxiliary_meanings_whitelist, value)
    def set_auxiliary_meanings_blacklist(self, value:str) -> None: self.set_field(NoteFields.NoteFields.auxiliary_meanings_blacklist, value)

    def update_from_wani(self, wani_model: models.Subject):
        self.set_level(wani_model.level)
        self.set_subject_id(wani_model.id)
        self.set_lesson_position(wani_model.lesson_position)
        self.set_document_url(wani_model.document_url)

        my_learning_order = "level:{:02d}-lesson_position:{:03d}".format(self.get_level(), self.get_lesson_position())
        self._set_my_learning_order(my_learning_order)

        auxiliary_meanings_whitelist = [meaning.meaning for meaning in wani_model.auxiliary_meanings if
                                        meaning.type == "whitelist"]

        auxiliary_meanings_blacklist = [meaning.meaning for meaning in wani_model.auxiliary_meanings if
                                        meaning.type == "blacklist"]

        self.set_auxiliary_meanings_whitelist(", ".join(auxiliary_meanings_whitelist))
        self.set_auxiliary_meanings_blacklist(", ".join(auxiliary_meanings_blacklist))

    def delete(self) -> None:
        facade.col().remNotes([self._note.id])
        facade.col().save()

    def card_ids(self) -> Sequence[int]:
        return self._note.card_ids()
