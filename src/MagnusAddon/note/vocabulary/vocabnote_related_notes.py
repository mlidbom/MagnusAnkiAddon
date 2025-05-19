from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from note.notefields.json_object_field import JsonObjectField, JsonObjectSerializer
from sysutils import ex_json
from sysutils.ex_json import JsonReader

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteRelatedNotesSerializer(JsonObjectSerializer["VocabNoteRelatedNotesData"], Slots):
    def deserialize(self, json: str) -> VocabNoteRelatedNotesData:
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

class VocabNoteRelatedNotesData(Slots):
    serializer: VocabNoteRelatedNotesSerializer = VocabNoteRelatedNotesSerializer()
    def __init__(self, ergative_twin: str, derived_from: str, derived: set[str], similar: set[str], antonyms: set[str], confused_with: set[str]) -> None:
        self.ergative_twin: str = ergative_twin
        self.derived_from: str = derived_from

        self.derived: set[str] = derived
        self.similar: set[str] = similar
        self.antonyms: set[str] = antonyms
        self.confused_with: set[str] = confused_with

class VocabErgativeTwin(Slots):
    def __init__(self, vocab: WeakRef[VocabNote], data: JsonObjectField[VocabNoteRelatedNotesData]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._data: JsonObjectField[VocabNoteRelatedNotesData] = data

    def get(self) -> str: return self._data.get().ergative_twin

    def set(self, value: str) -> None:
        self._data.get().ergative_twin = value

        for twin in app.col().vocab.with_question(value):
            if twin.related_notes.ergative_twin.get() != self._vocab().get_question():
                twin.related_notes.ergative_twin.set(self._vocab().get_question())

