from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.json_object_field import JsonObjectSerializer
from sysutils.json import ex_json
from sysutils.json.json_reader import JsonReader

if TYPE_CHECKING:
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingRulesData

class VocabNoteMatchingRulesSerializer(JsonObjectSerializer["VocabNoteMatchingRulesData"], Slots):
    def deserialize(self, json: str) -> VocabNoteMatchingRulesData:
        from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingRulesData
        if not json: return VocabNoteMatchingRulesData(set(), set(), set(), set())

        reader = JsonReader.from_json(json)
        return VocabNoteMatchingRulesData(reader.string_set("surface_is_not"),
                                          reader.string_set("prefer_over_base"),
                                          reader.string_set("prefix_is_not"),
                                          reader.string_set("required_prefix"))

    def serialize(self, rules: VocabNoteMatchingRulesData) -> str:
        return ex_json.dict_to_json({"surface_is_not": list(rules.surface_is_not),
                                     "prefer_over_base": list(rules.prefer_over_base),
                                     "prefix_is_not": list(rules.prefix_is_not),
                                     "required_prefix": list(rules.required_prefix)})
