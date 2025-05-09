from __future__ import annotations
from typing import Any, TYPE_CHECKING

from note.note_constants import SentenceNoteFields
from note.notefields.string_note_field import StringField
from sysutils import ex_json

if TYPE_CHECKING:
    from note.sentencenote import SentenceNote
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

_f_highlighted_words = 'highlighted_words'
_f_incorrect_matches = 'incorrect_matches'
class CachingSentenceConfigurationField:

    def __init__(self, note: SentenceNote) -> None:
        self._field = StringField(note, SentenceNoteFields.configuration)

        json = self._field.get()
        reader = ex_json.json_to_dict(json) if json else None
        self.highlighted_words: list[str] = reader.get_string_list(_f_highlighted_words) if reader else []
        self.incorrect_matches: list[WordExclusion] = \
            [WordExclusion.from_dict(exclusion_data)
             for exclusion_data in reader.get_nested_object_list(_f_incorrect_matches)] if reader else []

    def to_dict(self) -> dict[str, Any]:
        return {_f_highlighted_words: self.highlighted_words,
                _f_incorrect_matches: [exclusion.to_dict() for exclusion in self.incorrect_matches]}

    def incorrect_matches_words(self) -> set[str]:
        return {exclusion.word for exclusion in self.incorrect_matches}

    def to_json(self) -> str:
        return ex_json.dict_to_json(self.to_dict())
