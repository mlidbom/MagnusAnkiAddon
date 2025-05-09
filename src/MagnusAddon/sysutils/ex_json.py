from __future__ import annotations

import json
from typing import Any

from sysutils import typed

def dict_to_json(object_dict:dict[str, Any]) -> str:
    return json.dumps(object_dict, sort_keys=True, indent=3, ensure_ascii=False)

def json_to_dict(json_str:str) -> JsonDictReader:
    return JsonDictReader(typed.checked_cast_generics(dict[str, Any], json.loads(json_str)))

class JsonDictReader:
    def __init__(self, json_dict:dict[str, Any]) -> None:
        self._dict = json_dict

    def get_string(self, string:str) -> str: return typed.str_(self._dict[string])
    def get_int(self, string: str) -> int: return typed.int_(self._dict[string])
    def get_string_list(self, string:str) -> list[str]: return typed.checked_cast_generics(list[str], self._dict[string])
    def get_nested_object_list(self, string: str) -> list[JsonDictReader]: return [JsonDictReader(dict) for dict in typed.checked_cast_generics(list[dict[str, Any]], self._dict[string])]