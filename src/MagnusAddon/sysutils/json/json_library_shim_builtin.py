from __future__ import annotations

import json
from typing import Any

from autoslot import Slots
from sysutils import typed
from sysutils.json.json_library_shim import JsonLibraryShim


# noinspection PyUnusedClass,PyUnusedFunction
class JsonLibraryShimBuiltInJson(JsonLibraryShim, Slots):
    def loads(self, json_str: str) -> dict[str, Any]: return typed.checked_cast_generics(dict[str, Any], json.loads(json_str))
    def dumps(self, object_dict: dict[str, Any], indent: int | None = None) -> str: return json.dumps(object_dict, indent=indent, ensure_ascii=False)
