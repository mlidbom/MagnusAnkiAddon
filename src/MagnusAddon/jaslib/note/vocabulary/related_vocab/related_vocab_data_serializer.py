from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper
from jaslib.note.notefields.json_object_field import ObjectSerializer
from jaslib.sysutils.json import ex_json
from jaslib.sysutils.json.json_reader import JsonReader
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from jaslib.note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData

class RelatedVocabDataSerializer(ObjectSerializer["RelatedVocabData"], Slots):
    def __init__(self) -> None:
        if RelatedVocabDataSerializer._empty_object_json == "":
            RelatedVocabDataSerializer._empty_object_json = self.serialize(self.deserialize(""))

    @override
    def deserialize(self, serialized: str) -> RelatedVocabData:
        from jaslib.note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
        if not serialized: return RelatedVocabData("", ValueWrapper(""), QSet(), QSet(), QSet(), QSet(), QSet())

        reader = JsonReader.from_json(serialized)
        return RelatedVocabData(reader.string("ergative_twin", ""),
                                ValueWrapper(reader.string("derived_from", "")),
                                reader.string_set("perfect_synonyms", []),
                                reader.string_set("synonyms", []),
                                reader.string_set("antonyms", []),
                                reader.string_set("confused_with", []),
                                reader.string_set("see_also", []))

    _empty_object_json: str = ""
    @override
    def serialize(self, instance: RelatedVocabData) -> str:
        json_dict: dict[str, Any] = {}  # pyright: ignore[reportExplicitAny]

        if instance.ergative_twin: json_dict["ergative_twin"] = instance.ergative_twin
        if instance.derived_from.get(): json_dict["derived_from"] = instance.derived_from.get()
        if instance.synonyms: json_dict["synonyms"] = list(instance.synonyms)
        if instance.perfect_synonyms: json_dict["perfect_synonyms"] = list(instance.perfect_synonyms)
        if instance.antonyms: json_dict["antonyms"] = list(instance.antonyms)
        if instance.confused_with: json_dict["confused_with"] = list(instance.confused_with)
        if instance.see_also: json_dict["see_also"] = list(instance.see_also)

        json = ex_json.dict_to_json(json_dict)
        return json if json != RelatedVocabDataSerializer._empty_object_json else ""
