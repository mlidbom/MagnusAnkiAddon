from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper
from note.notefields.json_object_field import ObjectSerializer
from sysutils.json import ex_json
from sysutils.json.json_reader import JsonReader

if TYPE_CHECKING:
    from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData

class RelatedVocabDataSerializer(ObjectSerializer["RelatedVocabData"], Slots):
    @override
    def deserialize(self, serialized: str) -> RelatedVocabData:
        from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
        if not serialized: return RelatedVocabData("", ValueWrapper(""), set(), set(), set(), set(), set())

        reader = JsonReader.from_json(serialized)
        return RelatedVocabData(reader.string("ergative_twin"),
                                ValueWrapper(reader.string("derived_from")),
                                reader.string_set("perfect_synonyms", default=set()),
                                reader.string_set("synonyms"),
                                reader.string_set("antonyms"),
                                reader.string_set("confused_with"),
                                reader.string_set("see_also"))

    @override
    def serialize(self, instance: RelatedVocabData) -> str:
        return ex_json.dict_to_json({"ergative_twin": instance.ergative_twin,
                                     "derived_from": instance.derived_from.get(),
                                     "synonyms": list(instance.synonyms),
                                     "perfect_synonyms": list(instance.perfect_synonyms),
                                     "antonyms": list(instance.antonyms),
                                     "confused_with": list(instance.confused_with),
                                     "see_also": list(instance.see_also)})
