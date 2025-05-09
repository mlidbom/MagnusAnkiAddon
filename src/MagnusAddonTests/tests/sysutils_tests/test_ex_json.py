from __future__ import annotations

from sysutils import ex_json
from sysutils.ex_json import JsonDictReader

class IntObject:
    def __init__(self, value: int):
        self.value = value

    def to_dict(self) -> dict[str, int]:
        return {'value': self.value}

    @staticmethod
    def from_json(reader: JsonDictReader) -> IntObject:
        return IntObject(reader.get_int('value'))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IntObject):
            return False
        return self.value == other.value

    def __repr__(self) -> str:
        return f"IntObject({self.value})"

class HasObjectList:
    def __init__(self, values: list[IntObject]):
        self.values = values

    def to_dict(self) -> dict[str, list[dict[str, int]]]:
        return {'values': [value.to_dict() for value in self.values]}

    @staticmethod
    def from_json(reader: JsonDictReader) -> HasObjectList:
        return HasObjectList([IntObject.from_json(reader) for reader in reader.get_object_list('values')])

def test_round_object_list() -> None:
    start_value = HasObjectList([IntObject(1), IntObject(2), IntObject(3)])
    json = ex_json.dict_to_json(start_value.to_dict())
    round_tripped_value = HasObjectList.from_json(ex_json.json_to_dict(json))

    assert start_value.values == round_tripped_value.values
