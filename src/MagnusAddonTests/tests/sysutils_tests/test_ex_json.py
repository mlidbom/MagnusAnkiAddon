from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules  # noqa
from note.sentences.sentence_configuration import SentenceConfiguration
from note.sentences.word_exclusion_set import WordExclusionSet
from sysutils import ex_json

if TYPE_CHECKING:
    from sysutils.ex_json import JsonDictReader



class IntObject:
    def __init__(self, value: int) -> None:
        self.value = value

    def to_dict(self) -> dict[str, int]:
        return {"value": self.value}

    @staticmethod
    def from_json(reader: JsonDictReader) -> IntObject:
        return IntObject(reader.int("value"))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IntObject):
            return False
        return self.value == other.value

    def __repr__(self) -> str:
        return f"IntObject({self.value})"

class HasObjectList:
    def __init__(self, values: list[IntObject]) -> None:
        self.values = values

    def to_dict(self) -> dict[str, list[dict[str, int]]]:
        return {"values": [value.to_dict() for value in self.values]}

    @staticmethod
    def from_json(reader: JsonDictReader) -> HasObjectList:
        return HasObjectList(reader.object_list("values",IntObject.from_json))

def test_round_object_list() -> None:
    start_value = HasObjectList([IntObject(1), IntObject(2), IntObject(3)])
    json = ex_json.dict_to_json(start_value.to_dict())
    round_tripped_value = HasObjectList.from_json(ex_json.json_to_reader(json))

    assert start_value.values == round_tripped_value.values

def test_roundtrip_parsing_result() -> None:
    from note.sentences.parsed_word import ParsedWord
    from note.sentences.parsing_result import ParsingResult

    parsing_result = ParsingResult([ParsedWord("foo"), ParsedWord("bar")], "foo bar", "1.0")
    json = ex_json.dict_to_json(ParsingResult.serializer.to_dict(parsing_result))
    round_tripped_result = ParsingResult.serializer.from_reader(ex_json.json_to_reader(json))

    assert [w.word for w in parsing_result.parsed_words] == [w.word for w in round_tripped_result.parsed_words]

def test_roundtrip_configuration() -> None:
    from note.sentences.parsed_word import ParsedWord
    from note.sentences.parsing_result import ParsingResult

    result = ParsingResult([ParsedWord("foo"), ParsedWord("bar")], "foo bar", "1.0")
    config = SentenceConfiguration([], WordExclusionSet(lambda: None, []), WordExclusionSet(lambda: None, []), result)
    json = SentenceConfiguration.serializer.serialize(config)
    round_tripped_result = SentenceConfiguration.serializer.deserialize(json, lambda: None)

    assert [w.word for w in config.parsing_result.parsed_words] == [w.word for w in round_tripped_result.parsing_result.parsed_words]
