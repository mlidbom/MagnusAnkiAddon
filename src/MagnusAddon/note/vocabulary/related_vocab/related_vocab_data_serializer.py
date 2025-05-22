from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper
from note.notefields.json_object_field import JsonObjectSerializer
from sysutils.json import ex_json
from sysutils.json.json_reader import JsonReader

if TYPE_CHECKING:
    from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData


class RelatedVocabDataSerializer(JsonObjectSerializer["RelatedVocabData"], Slots):
    def deserialize(self, json: str) -> RelatedVocabData:
        from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
        if not json: return RelatedVocabData("", ValueWrapper(""), set(), set(), set(), set())

        reader = JsonReader.from_json(json)
        return RelatedVocabData(reader.string("ergative_twin"),
                                ValueWrapper(reader.string("derived_from")),
                                reader.string_set("synonyms"),
                                reader.string_set("antonyms"),
                                reader.string_set("confused_with"),
                                reader.string_set("see_also", default=set())) #todo: remove default after repopulation

    def serialize(self, related_notes: RelatedVocabData) -> str:
        return ex_json.dict_to_json({"ergative_twin": related_notes.ergative_twin,
                                     "derived_from": related_notes.derived_from.get(),
                                     "synonyms": list(related_notes.synonyms),
                                     "antonyms": list(related_notes.antonyms),
                                     "confused_with": list(related_notes.confused_with),
                                     "see_also": list(related_notes.see_also)})
