# from __future__ import annotations
#
# from typing import Any
#
# from ex_autoslot import ProfilableAutoSlots
# from sysutils.json.json_library_shim import JsonLibraryShim
#
#
# # noinspection PyUnusedClass,PyUnusedFunction
# class JsonLibraryShimOrjson(JsonLibraryShim, ProfilableAutoSlots):
#     def __init__(self) -> None:
#         import orjson
#
#         self.orjson = orjson
#
#     def loads(self, json_str: str) -> dict[str, Any]:
#         return self.orjson.loads(json_str)
#
#     def dumps(self, object_dict: dict[str, Any], indent: int | None = None) -> str:
#         options = 0
#         if indent is not None:
#             options = self.orjson.OPT_INDENT_2
#         return self.orjson.dumps(object_dict, option=options).decode("utf-8")
