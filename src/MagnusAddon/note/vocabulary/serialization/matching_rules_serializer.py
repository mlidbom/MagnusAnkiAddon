from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.notefields.json_object_field import ObjectSerializer
from sysutils.json import ex_json
from sysutils.json.json_reader import JsonReader

if TYPE_CHECKING:
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingRulesData

class VocabNoteMatchingRulesSerializer(ObjectSerializer["VocabNoteMatchingRulesData"], Slots):
    @override
    def deserialize(self, serialized: str) -> VocabNoteMatchingRulesData:
        from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingRulesData
        if not serialized: return VocabNoteMatchingRulesData(set(), set(), set(), set(), set())

        reader = JsonReader.from_json(serialized)
        return VocabNoteMatchingRulesData(reader.string_set("surface_is_not"),
                                          reader.string_set("prefix_is_not"),
                                          reader.string_set("suffix_is_not", set()),
                                          reader.string_set("required_prefix"),
                                          reader.string_set("yield_to_surface", set()))

    @override
    def serialize(self, instance: VocabNoteMatchingRulesData) -> str:
        return ex_json.dict_to_json({"surface_is_not": list(instance.surface_is_not),
                                     "prefix_is_not": list(instance.prefix_is_not),
                                     "suffix_is_not": list(instance.suffix_is_not),
                                     "required_prefix": list(instance.required_prefix),
                                     "yield_to_surface": list(instance.yield_to_surface)})
