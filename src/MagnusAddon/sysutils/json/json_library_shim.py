from __future__ import annotations

from typing import Any

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]


# noinspection PyUnusedFunction
class JsonLibraryShim(Slots):
    def loads(self, json_str: str) -> dict[str, Any]: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter, reportExplicitAny]
    def dumps(self, object_dict: dict[str, Any], indent: int | None = None) -> str: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter, reportExplicitAny]
