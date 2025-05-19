from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.json_object_field import JsonObjectSerializer
from sysutils import ex_json
from sysutils.ex_json import JsonReader

if TYPE_CHECKING:
    from note.vocabulary.related_notes.related_notes_data import VocabNoteRelatedNotesData


class VocabNoteRelatedNotesSerializer(JsonObjectSerializer["VocabNoteRelatedNotesData"], Slots):
    def deserialize(self, json: str) -> VocabNoteRelatedNotesData:
        from note.vocabulary.related_notes.related_notes_data import VocabNoteRelatedNotesData
        if not json: return VocabNoteRelatedNotesData("", "", set(), set(), set(), set())

        reader = JsonReader.from_json(json)
        return VocabNoteRelatedNotesData(reader.string("ergative_twin"),
                                         reader.string("derived_from"),
                                         reader.string_set("derived"),
                                         reader.string_set("similar"),
                                         reader.string_set("antonyms"),
                                         reader.string_set("confused_with"))

    def serialize(self, related_notes: VocabNoteRelatedNotesData) -> str:
        return ex_json.dict_to_json({"ergative_twin": related_notes.ergative_twin,
                                     "derived_from": related_notes.derived_from,
                                     "derived": list(related_notes.derived),
                                     "similar": list(related_notes.similar),
                                     "antonyms": list(related_notes.antonyms),
                                     "confused_with": list(related_notes.confused_with)})
