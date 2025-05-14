from __future__ import annotations

from ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules  # noqa
from deepdiff import DeepDiff
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.sentences.sentence_configuration import SentenceConfiguration
from note.sentences.word_exclusion_set import WordExclusionSet
from sysutils import ex_json
from sysutils.ex_json import JsonReader


class IntObject:
    def __init__(self, value: int) -> None:
        self.value = value

    def to_dict(self) -> dict[str, int]:
        return {"value": self.value}

    @staticmethod
    def from_json(reader: JsonReader) -> IntObject:
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
    def from_json(reader: JsonReader) -> HasObjectList:
        return HasObjectList(reader.object_list("values", IntObject.from_json))

def test_round_object_list() -> None:
    start_value = HasObjectList([IntObject(1), IntObject(2), IntObject(3)])
    json = ex_json.dict_to_json(start_value.to_dict())
    round_tripped_value = HasObjectList.from_json(JsonReader.from_json(json))

    assert_object_graphs_identical(start_value, round_tripped_value)

def test_roundtrip_parsing_result() -> None:
    from note.sentences.parsed_word import ParsedWord
    from note.sentences.parsing_result import ParsingResult

    parsing_result = ParsingResult([ParsedWord("foo"), ParsedWord("bar")], "foo bar", "1.0")
    json = ParsingResult.serializer.serialize(parsing_result)
    round_tripped_result = ParsingResult.serializer.deserialize(json)

    assert_object_graphs_identical(parsing_result, round_tripped_result)

def test_roundtrip_configuration() -> None:
    config = SentenceConfiguration(["1", "2"],
                                   WordExclusionSet(lambda: None, [WordExclusion.global_("111"), WordExclusion.global_("222")]),
                                   WordExclusionSet(lambda: None, [WordExclusion.global_("333"), WordExclusion.global_("444")]))
    json = SentenceConfiguration.serializer.serialize(config)
    round_tripped_result = SentenceConfiguration.serializer.deserialize(json, lambda: None)
    assert_object_graphs_identical(config, round_tripped_result)

def assert_object_graphs_identical(expected: object, actual: object) -> None:
    diff = DeepDiff(expected, actual)
    if diff:
        raise AssertionError(diff)
