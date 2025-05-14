from __future__ import annotations

import json
from typing import Any, Callable, TypeVar

from sysutils import typed


def dict_to_json(object_dict: dict[str, Any], indent: int | None = None) -> str:
    return json.dumps(object_dict, ensure_ascii=False, indent=indent)

T: TypeVar = TypeVar("T")

class JsonReader:
    def __init__(self, json_dict: dict[str, Any]) -> None:
        self._dict = json_dict

    def string(self, prop: str) -> str: return typed.str_(self._dict[prop])
    def int(self, prop: str) -> string: return typed.int_(self._dict[prop])
    def string_list(self, string: str) -> list[str]: return typed.checked_cast_generics(list[str], self._dict[string])

    def object_list(self, prop: str, factory: Callable[[JsonReader], T], allow_missing: bool = False) -> list[T]:
        prop_value = self._dict.get(prop, None)
        if prop_value is None and allow_missing:
            return []

        reader_list = [JsonReader(json_dict) for json_dict in typed.checked_cast_generics(list[dict[str, Any]], prop_value)]

        return [factory(reader) for reader in reader_list]

    # noinspection PyUnusedFunction
    def object(self, prop: str, factory: Callable[[JsonReader], T], default: Callable[[], T] | None = None) -> T | None:
        reader = self._reader_or_none(prop)
        return default() if reader is None and default is not None else factory(typed.non_optional(reader))

    def _reader_or_none(self, prop: str) -> JsonReader | None:
        dict_ = self._dict.get(prop, None)
        return None if dict_ is None else JsonReader(typed.checked_cast_generics(dict[str, Any], dict_))

    @classmethod
    def from_json(cls, json_str: str) -> JsonReader:
        return cls(typed.checked_cast_generics(dict[str, Any], json.loads(json_str)))
