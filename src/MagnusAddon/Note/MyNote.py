from anki.notes import Note


class MyNote:
    def __init__(self, note: Note):
        self._note = note

    def _assert_field_exists(self, field_name: str):
        if self._note[field_name] is None:
            raise ValueError("No field named:" + field_name)

    def get_field(self, field_name: str) -> str:
        self._assert_field_exists(field_name)
        return self._note[field_name]

    def set_field(self, field_name: str, value: str) -> None:
        field_value = self._note[field_name]
        if field_value is None: raise ValueError("No field named:" + field_name)
        if field_value != value:
            self._note[field_name] = value
            self._note.flush()
