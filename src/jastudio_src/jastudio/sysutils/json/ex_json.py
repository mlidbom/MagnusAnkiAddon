from __future__ import annotations

from typing import Any

from jastudio.sysutils.json.json_library_shim_builtin import JsonLibraryShimBuiltInJson

#from jastudio.sysutils.json.json_library_shim_orjson import JsonLibraryShimOrjson

json_library_shim = JsonLibraryShimBuiltInJson()
# To use orjson instead, uncomment the following line:
#_json_library_shim = JsonLibraryShimOrjson()


def dict_to_json(object_dict: dict[str, Any], indent: int | None = None) -> str:  # pyright: ignore[reportExplicitAny]
    return json_library_shim.dumps(object_dict, indent=indent)

