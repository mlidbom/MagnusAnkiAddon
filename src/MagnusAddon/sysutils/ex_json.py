from __future__ import annotations

import json
from typing import Any, Callable, TypeVar

from autoslot import Slots
from sysutils import typed


def dict_to_json(object_dict: dict[str, Any], indent: int | None = None) -> str:
    return json.dumps(object_dict, ensure_ascii=False, indent=indent)

TProp: TypeVar = TypeVar("TProp")

class JsonReader(Slots):
    def __init__(self, json_dict: dict[str, Any]) -> None:
        self._dict = json_dict

    def _get_prop(self, prop: str | list[str], prop_type: type[TProp], default: TProp | None) -> TProp:
        if isinstance(prop, str):
            return typed.checked_cast_generics(prop_type, self._dict.get(prop, None))

        for p in prop:
            if p in self._dict:
                return typed.checked_cast_generics(prop_type, self._dict[p])

        if default is None:
            raise KeyError(f"None of the following keys were found in the JSON: {prop}")

        return default

    def string(self, prop: str | list[str], default: str | None = None) -> str: return self._get_prop(prop, str, default)
    def int(self, prop: str | list[str], default: int | None = None) -> string: return self._get_prop(prop, int, default)

    def string_list(self, prop: str | list[str], default: list[str] | None = None) -> list[str]:
        return self._get_prop(prop, list[str], default)

    def string_set(self, prop: str | list[str], default: set[str] | None = None) -> set[str]: return set(self.string_list(prop, default))

    def object_list(self, prop: str | list[str], factory: Callable[[JsonReader], TProp], default: list[TProp] | None = None) -> list[TProp]:
        prop_value = self._get_prop(prop, list[dict[str, Any]], default)
        reader_list = [JsonReader(json_dict) for json_dict in prop_value]
        return [factory(reader) for reader in reader_list]

    # noinspection PyUnusedFunction
    def object(self, prop: str, factory: Callable[[JsonReader], TProp], default: Callable[[], TProp] | None = None) -> TProp | None:
        reader = self._reader_or_none(prop)
        return default() if reader is None and default is not None else factory(typed.non_optional(reader))

    def _reader_or_none(self, prop: str) -> JsonReader | None:
        dict_ = self._dict.get(prop, None)
        return None if dict_ is None else JsonReader(typed.checked_cast_generics(dict[str, Any], dict_))

    @classmethod
    def from_json(cls, json_str: str) -> JsonReader:
        return cls(typed.checked_cast_generics(dict[str, Any], json.loads(json_str)))
