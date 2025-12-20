from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from autoslot import Slots  # type: ignore[reportMissingTypeStubs]
from note.sentences.word_exclusion_set import WordExclusionSet
from sysutils.json import ex_json
from sysutils.json.json_reader import JsonReader

if TYPE_CHECKING:
    from collections.abc import Callable

    from note.sentences.sentence_configuration import SentenceConfiguration

class SentenceConfigurationSerializer(Slots):
    @staticmethod
    def deserialize(json: str, save_callback: Callable[[], None]) -> SentenceConfiguration:
        from note.sentences.sentence_configuration import SentenceConfiguration
        if not json: return SentenceConfiguration(set(), WordExclusionSet(save_callback, []), WordExclusionSet(save_callback, []))

        reader = JsonReader.from_json(json)
        return SentenceConfiguration(reader.string_set("highlighted_words"),
                                     WordExclusionSet(save_callback, reader.object_list("incorrect_matches", WordExclusion.from_reader)),
                                     WordExclusionSet(save_callback, reader.object_list("hidden_matches", WordExclusion.from_reader)))

    @staticmethod
    def serialize(config: SentenceConfiguration) -> str:
        return ex_json.dict_to_json({"highlighted_words": list(config.highlighted_words),
                                     "incorrect_matches": [exclusion.to_dict() for exclusion in config.incorrect_matches.get()],
                                     "hidden_matches": [exclusion.to_dict() for exclusion in config.hidden_matches.get()]})
