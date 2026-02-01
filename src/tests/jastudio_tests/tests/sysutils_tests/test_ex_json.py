from __future__ import annotations

from typing import override

from anki.notes import NoteId
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from deepdiff import DeepDiff
from jastudio.ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules  # noqa  # pyright: ignore[reportUnusedImport]
from jastudio.language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from jastudio.note.sentences.sentence_configuration import SentenceConfiguration
from jastudio.note.sentences.word_exclusion_set import WordExclusionSet
from jastudio.sysutils.json import ex_json
from jastudio.sysutils.json.json_reader import JsonReader
from typed_linq_collections.collections.q_unique_list import QUniqueList


class IntObject(Slots):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def to_dict(self) -> dict[str, int]:
        return {"value": self.value}

    @classmethod
    def from_json(cls, reader: JsonReader) -> IntObject:
        return IntObject(reader.integer("value"))

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IntObject):
            return False
        return self.value == other.value

    @override
    def __repr__(self) -> str:
        return f"IntObject({self.value})"

class HasObjectList(Slots):
    def __init__(self, values: list[IntObject]) -> None:
        self.values: list[IntObject] = values

    def to_dict(self) -> dict[str, list[dict[str, int]]]:
        return {"values": [value.to_dict() for value in self.values]}

    @classmethod
    def from_json(cls, reader: JsonReader) -> HasObjectList:
        return HasObjectList(reader.object_list("values", IntObject.from_json))

def test_round_object_list() -> None:
    start_value = HasObjectList([IntObject(1), IntObject(2), IntObject(3)])
    json = ex_json.dict_to_json(start_value.to_dict())
    round_tripped_value = HasObjectList.from_json(JsonReader.from_json(json))

    assert_object_graphs_identical(start_value, round_tripped_value)

def test_roundtrip_parsing_result() -> None:
    from jastudio.note.sentences.parsed_match import ParsedMatch
    from jastudio.note.sentences.parsing_result import ParsingResult

    parsing_result = ParsingResult([ParsedMatch("B", 0, True, "foo", NoteId(1)), #the information string is not read when loading so don't set it to anything
                                    ParsedMatch("B", 4, False, "bar", NoteId(2))], "foo bar", "1.0") #the information string is not read when loading so don't set it to anything
    serialized = ParsingResult.serializer.serialize(parsing_result)
    round_tripped_result = ParsingResult.serializer.deserialize(serialized)

    assert_object_graphs_identical(parsing_result, round_tripped_result)

def test_roundtrip_configuration() -> None:
    config = SentenceConfiguration(QUniqueList({"1", "2"}),
                                   WordExclusionSet(lambda: None, [WordExclusion.global_("111"), WordExclusion.global_("222")]),
                                   WordExclusionSet(lambda: None, [WordExclusion.global_("333"), WordExclusion.global_("444")]))
    json = SentenceConfiguration.serializer().serialize(config)
    round_tripped_result = SentenceConfiguration.serializer().deserialize(json, lambda: None)
    assert_object_graphs_identical(config, round_tripped_result)

def assert_object_graphs_identical(expected: object, actual: object) -> None:
    diff = DeepDiff(expected, actual)
    if diff:
        raise AssertionError(diff)
