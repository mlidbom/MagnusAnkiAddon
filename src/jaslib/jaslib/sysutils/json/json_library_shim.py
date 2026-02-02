from __future__ import annotations

from typing import Any

from autoslot import Slots
from jaslib.sysutils.abstract_method_called_error import AbstractMethodCalledError


# noinspection PyUnusedFunction
class JsonLibraryShim(Slots):
    # noinspection Annotator
    def loads(self, json_str: str) -> dict[str, Any]: raise AbstractMethodCalledError()  # pyright: ignore[reportUnusedParameter, reportExplicitAny]
    # noinspection Annotator
    def dumps(self, object_dict: dict[str, Any], indent: int | None = None) -> str: raise AbstractMethodCalledError()  # pyright: ignore[reportUnusedParameter, reportExplicitAny]
