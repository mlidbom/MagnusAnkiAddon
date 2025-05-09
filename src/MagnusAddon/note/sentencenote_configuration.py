from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from note.note_constants import SentenceNoteFields
from note.notefields.string_note_field import StringField
from sysutils import ex_json

if TYPE_CHECKING:
    from note.sentencenote import SentenceNote
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

class SentenceConfiguration:
    def __init__(self, json:str) -> None:
        reader = ex_json.json_to_dict(json) if json else None
        self.highlighted_words: list[str] = reader.get_string_list(_f_highlighted_words) if reader else []
        self.incorrect_matches: list[WordExclusion] = \
            [WordExclusion.from_dict(exclusion_data)
             for exclusion_data in reader.get_nested_object_list(_f_incorrect_matches)] if reader else []

_f_highlighted_words = 'highlighted_words'
_f_incorrect_matches = 'incorrect_matches'
class CachingSentenceConfigurationField:

    def __init__(self, note: SentenceNote) -> None:
        self._field = StringField(note, SentenceNoteFields.configuration)
        self._value:Optional[SentenceConfiguration] = None

    def get(self) -> SentenceConfiguration:
        if self._value is None:
            self._value = SentenceConfiguration(self._field.get())
        return self._value

    def incorrect_matches_words(self) -> set[str]:
        return {exclusion.word for exclusion in self.get().incorrect_matches}

    def _save(self) -> None:
        self._field.set(ex_json.dict_to_json({_f_highlighted_words: self.get().highlighted_words,
                                              _f_incorrect_matches: [exclusion.to_dict() for exclusion in self.get().incorrect_matches]}))


