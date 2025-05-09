from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils import ex_str

if TYPE_CHECKING:
    from note.jpnote import JPNote

class StringField:
    def __init__(self, note:JPNote, field_name:str) -> None:
        self._note = note
        self._field_name = field_name

    def set(self, value:str) -> None:
        self._note.set_field(self._field_name, value.strip())

    def get(self) -> str: return self._note.get_field(self._field_name).strip()

class StripHtmlOnReadStringField:
    def __init__(self, note:JPNote, field_name:str) -> None:
        self._field = StringField(note, field_name)

    def get(self) -> str: return ex_str.strip_html_markup(self._field.get())
    def set(self, value:str) -> None: self._field.set(value)

class FallbackStringField:
    def __init__(self, note:JPNote, primary_field:str, fallback_field:str) -> None:
        self._field = StringField(note, primary_field)
        self._fallback_field = StringField(note, fallback_field)

    def get(self) -> str: return self._field.get() or self._fallback_field.get()

class StringListField:
    def __init__(self, note:JPNote, field_name:str) -> None:
        self._field = StringField(note, field_name)

    def get(self) -> list[str]: return ex_str.extract_comma_separated_values(self._field.get())
    def set(self, value:list[str]) -> None: self._field.set(ex_str.to_comma_separated_values(value))

class StringSetField:
    def __init__(self, note:JPNote, field_name:str) -> None:
        self._field = StringListField(note, field_name)

    def get(self) -> set[str]: return set(self._field.get())
    def set(self, value:set[str]) -> None: self._field.set(list(value))

class AudioField(StripHtmlOnReadStringField):
    def __init__(self, note:JPNote, field_name:str) -> None:
        super().__init__(note, field_name)

    def file_path(self) -> str: return self.get()[7:-1]

class ReadOnlyNewlineSeparatedValuesField:
    def __init__(self, note:JPNote, field_name:str) -> None:
        self._field = StringField(note, field_name)

    def get(self) -> list[str]: return ex_str.extract_newline_separated_values(self._field.get())


