from __future__ import annotations

import json
from typing import Any, cast, override

from ex_autoslot import AutoSlots
from sysutils.json.json_library_shim import JsonLibraryShim


# noinspection PyUnusedClass,PyUnusedFunction
class JsonLibraryShimBuiltInJson(JsonLibraryShim, AutoSlots):
    @override
    def loads(self, json_str: str) -> dict[str, Any]: return cast(dict[str, Any], json.loads(json_str))  # pyright: ignore[reportExplicitAny]
    @override
    def dumps(self, object_dict: dict[str, Any], indent: int | None = None) -> str: return json.dumps(object_dict, indent=indent, ensure_ascii=False)  # pyright: ignore[reportExplicitAny]
