from __future__ import annotations

from typing import TYPE_CHECKING, Any

from autoslot import Slots
from jaslib.language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from jaslib.note.sentences.word_exclusion_set import WordExclusionSet
from jaslib.sysutils.json import ex_json
from jaslib.sysutils.json.json_reader import JsonReader
from typed_linq_collections.collections.q_unique_list import QUniqueList

if TYPE_CHECKING:
    from collections.abc import Callable

    from jaslib.note.sentences.sentence_configuration import SentenceConfiguration

class SentenceConfigurationSerializer(Slots):
    def __init__(self) -> None:
        if SentenceConfigurationSerializer._empty_object_json == "":
            SentenceConfigurationSerializer._empty_object_json = self.serialize(self.deserialize("", lambda: None))

    # noinspection PyMethodMayBeStatic
    def deserialize(self, json: str, save_callback: Callable[[], None]) -> SentenceConfiguration:
        from jaslib.note.sentences.sentence_configuration import SentenceConfiguration
        if not json: return SentenceConfiguration(QUniqueList(), WordExclusionSet(save_callback, []), WordExclusionSet(save_callback, []))

        reader = JsonReader.from_json(json)
        return SentenceConfiguration(QUniqueList(reader.string_set("highlighted_words", [])),
                                     WordExclusionSet(save_callback, reader.object_list("incorrect_matches", WordExclusion.from_reader, [])),
                                     WordExclusionSet(save_callback, reader.object_list("hidden_matches", WordExclusion.from_reader, [])))

    _empty_object_json: str = ""
    # noinspection PyMethodMayBeStatic
    def serialize(self, config: SentenceConfiguration) -> str:
        json_dict: dict[str, Any] = {} # pyright: ignore[reportExplicitAny]
        if config.highlighted_words.any(): json_dict["highlighted_words"] = list(config.highlighted_words)
        if config.incorrect_matches.words().any(): json_dict["incorrect_matches"] = [exclusion.to_dict() for exclusion in config.incorrect_matches.get()]
        if config.hidden_matches.get().any(): json_dict["hidden_matches"] = [exclusion.to_dict() for exclusion in config.hidden_matches.get()]
        json = ex_json.dict_to_json(json_dict)

        return json if json != SentenceConfigurationSerializer._empty_object_json else ""
