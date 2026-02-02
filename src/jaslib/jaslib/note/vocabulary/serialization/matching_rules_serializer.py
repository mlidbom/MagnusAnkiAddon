from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from autoslot import Slots
from jaslib.note.notefields.json_object_field import ObjectSerializer
from jaslib.sysutils.json import ex_json
from jaslib.sysutils.json.json_reader import JsonReader
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from jaslib.note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingRulesData

class VocabNoteMatchingRulesSerializer(ObjectSerializer["VocabNoteMatchingRulesData"], Slots):
    def __init__(self) -> None:
        if VocabNoteMatchingRulesSerializer._empty_object_json == "":
            VocabNoteMatchingRulesSerializer._empty_object_json = self.serialize(self.deserialize(""))

    @override
    def deserialize(self, serialized: str) -> VocabNoteMatchingRulesData:
        from jaslib.note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingRulesData
        if not serialized: return VocabNoteMatchingRulesData(QSet(), QSet(), QSet(), QSet(), QSet())

        reader = JsonReader.from_json(serialized)
        return VocabNoteMatchingRulesData(reader.string_set("surface_is_not", []),
                                          reader.string_set("prefix_is_not", []),
                                          reader.string_set("suffix_is_not", []),
                                          reader.string_set("required_prefix", []),
                                          reader.string_set("yield_to_surface", []))

    _empty_object_json: str = ""
    @override
    def serialize(self, instance: VocabNoteMatchingRulesData) -> str:
        json_dict: dict[str, Any] = {}  # pyright: ignore[reportExplicitAny]

        if instance.surface_is_not: json_dict["surface_is_not"] = list(instance.surface_is_not)
        if instance.prefix_is_not: json_dict["prefix_is_not"] = list(instance.prefix_is_not)
        if instance.suffix_is_not: json_dict["suffix_is_not"] = list(instance.suffix_is_not)
        if instance.required_prefix: json_dict["required_prefix"] = list(instance.required_prefix)
        if instance.yield_to_surface: json_dict["yield_to_surface"] = list(instance.yield_to_surface)

        json = ex_json.dict_to_json(json_dict)

        return json if json != VocabNoteMatchingRulesSerializer._empty_object_json else ""
