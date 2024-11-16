from wanikani_api import models
from anki.notes import Note
from note.jpnote import JPNote
from note.note_constants import Mine, NoteFields


class WaniNote(JPNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def _set_level_tag(self, new_level: int) -> None:
        level_tags = [level for level in self._note.tags if level.startswith(Mine.Tags.wani_level)]
        for level in level_tags:
            self._note.remove_tag(level)
        self.set_tag(f"""{Mine.Tags.wani_level}{"{:02d}".format(new_level)}""")

    def get_subject_id(self) -> int: return int(self.get_field(NoteFields.WaniCommon.subject_id))
    def _set_subject_id(self, value: int) -> None: self.set_field(NoteFields.WaniCommon.subject_id, str(value))

    def get_lesson_position(self) -> int:
        if not self.is_wani_note(): return 0
        return int(self.get_field(NoteFields.WaniCommon.lesson_position))

    def _set_lesson_position(self, value: int) -> None:
        current_position = self.get_field(NoteFields.WaniCommon.lesson_position)

        # Wani api does some weird stuff sometimes returning 0 as lesson positions for many subjects.
        # Possibly the ones in the current level or currently being studied.
        # Anyway, we do NOT want to overwrite valid lesson positions with zeroes!
        if value > 0:
            self.set_field(NoteFields.WaniCommon.lesson_position, str(value))
        else:
            if current_position == "0" or current_position == "" or current_position is None:
                self.set_field(NoteFields.WaniCommon.lesson_position, str(value))
            else:
                print("Ignoring 0 as value for lesson_position for subject: {}".format(self.get_subject_id()))


    def _set_my_learning_order(self, value: str) -> None: self.set_field(NoteFields.WaniCommon.my_learning_order, value)
    def set_document_url(self, value: str) -> None: self.set_field(NoteFields.WaniCommon.document_url, value)

    def get_level(self) -> int:
        if not self.is_wani_note():
            return 0 #non wani items
        return int(self.get_field(NoteFields.WaniCommon.level))

    def _set_level(self, value: int) -> None:
        self._set_level_tag(value)
        self.set_field(NoteFields.WaniCommon.level, str(value))

    def set_auxiliary_meanings_whitelist(self, value:str) -> None: self.set_field(NoteFields.WaniCommon.auxiliary_meanings_whitelist, value)
    def set_auxiliary_meanings_blacklist(self, value:str) -> None: self.set_field(NoteFields.WaniCommon.auxiliary_meanings_blacklist, value)

    def update_from_wani(self, wani_model: models.Subject) -> None:
        self._set_level(wani_model.level)
        self._set_subject_id(wani_model.id)
        self._set_lesson_position(wani_model.lesson_position)
        self.set_document_url(wani_model.document_url)

        my_learning_order = "level:{:02d}-lesson_position:{:03d}".format(self.get_level(), self.get_lesson_position())
        self._set_my_learning_order(my_learning_order)

        auxiliary_meanings_whitelist = [meaning.meaning for meaning in wani_model.auxiliary_meanings if
                                        meaning.type == "whitelist"]

        auxiliary_meanings_blacklist = [meaning.meaning for meaning in wani_model.auxiliary_meanings if
                                        meaning.type == "blacklist"]

        self.set_auxiliary_meanings_whitelist(", ".join(auxiliary_meanings_whitelist))
        self.set_auxiliary_meanings_blacklist(", ".join(auxiliary_meanings_blacklist))
