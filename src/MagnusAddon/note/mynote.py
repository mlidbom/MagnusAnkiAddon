from anki.notes import Note


class MyNote:
    def __init__(self, note: Note):
        self._note = note


    def get_field(self, field_name: str) -> str: return self._note[field_name]

    def set_field(self, field_name: str, value: str) -> None:
        field_value = self._note[field_name]
        if field_value != value:
            self._note[field_name] = value
            self._note.flush()

    def has_tag(self, tag:str) -> bool: return tag in self._note.tags

    def set_tag(self, tag:str) -> None:
        if not self.has_tag(tag):
            self._note.tags.append(tag)
            self._note.flush()

    def last_edit_time(self) -> int:
        return self._note.mod