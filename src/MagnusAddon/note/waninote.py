from typing import Sequence

from wanikani_api import models
from anki.notes import Note

from ankiutils.anki_shim import get_anki_collection
from note.mynote import MyNote
from wanikani.wani_constants import Mine, Wani


class WaniNote(MyNote):
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

    def is_wani_note(self) -> bool:
        return Mine.Tags.Wani in self._note.tags

    def get_note_type_name(self) -> str:
        # noinspection PyProtectedMember
        return self._note._note_type['name']  # Todo: find how to do this without digging into protected members

    def get_sort_id(self) -> str: return self.get_field(Wani.NoteFields.sort_id)
    def set_sort_id(self, value: str) -> None: self.set_field(Wani.NoteFields.sort_id, value)

    def get_subject_id(self) -> int: return int(self.get_field(Wani.NoteFields.subject_id))
    def set_subject_id(self, value: int) -> None: self.set_field(Wani.NoteFields.subject_id, str(value))

    def get_lesson_position(self) -> int:
        if not self.is_wani_note(): return 0
        return int(self.get_field(Wani.NoteFields.lesson_position))

    def set_lesson_position(self, value: int) -> None:
        current_position = self.get_field(Wani.NoteFields.lesson_position)

        # Wani api does some weird stuff sometimes returning 0 as lesson positions for many subjects.
        # Possibly the ones in the current level or currently being studied.
        # Anyway, we do NOT want to overwrite valid lesson positions with zeroes!
        if value > 0:
            self.set_field(Wani.NoteFields.lesson_position, str(value))
        else:
            if current_position == "0" or current_position == "" or current_position is None:
                self.set_field(Wani.NoteFields.lesson_position, str(value))
            else:
                print("Ignoring 0 as value for lesson_position for subject: {}".format(self.get_subject_id()))


    def get_my_learning_order(self) -> str: return self.get_field(Wani.NoteFields.my_learning_order)
    def _set_my_learning_order(self, value: str) -> None: self.set_field(Wani.NoteFields.my_learning_order, value)

    def get_document_url(self) -> str: return self.get_field(Wani.NoteFields.document_url)
    def set_document_url(self, value: str) -> None: self.set_field(Wani.NoteFields.document_url, value)

    def get_level(self) -> int:
        if not self.is_wani_note():
            return 0 #non wani items
        return int(self.get_field(Wani.NoteFields.level))

    def set_level(self, value: int) -> None:
        self.set_level_tag(value)
        self.set_field(Wani.NoteFields.level, str(value))

    def set_auxiliary_meanings_whitelist(self, value:str) -> None: self.set_field(Wani.NoteFields.auxiliary_meanings_whitelist, value)
    def set_auxiliary_meanings_blacklist(self, value:str) -> None: self.set_field(Wani.NoteFields.auxiliary_meanings_blacklist, value)

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
        get_anki_collection().remNotes([self._note.id])
        get_anki_collection().save()

    def card_ids(self) -> Sequence[int]:
        return self._note.card_ids()
