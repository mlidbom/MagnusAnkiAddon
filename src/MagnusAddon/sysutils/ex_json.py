import json
from typing import Any

from sysutils import typed

def dict_to_json(object_dict:dict[str, Any]) -> str:
    return json.dumps(object_dict, sort_keys=True, indent=3, ensure_ascii=False)

def json_to_dict(json_str:str) -> dict[str, Any]:
    return typed.checked_cast_generics(dict[str, Any], json.loads(json_str))