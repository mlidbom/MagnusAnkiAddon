from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import SentenceNoteFields
from note.notefields.json_object_field import JsonObjectField
from note.sentences.parsing_result import ParsingResult
from note.sentences.serialization.parsing_result_serializer import ParsingResultSerializer

if TYPE_CHECKING:
    from note.sentences.sentencenote import SentenceNote


class ParsingResultField(JsonObjectField[ParsingResult]):
    def __init__(self, sentence: SentenceNote) -> None:
        super().__init__(sentence, SentenceNoteFields.parsing_result, ParsingResultSerializer())