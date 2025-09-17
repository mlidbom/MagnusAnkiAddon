from __future__ import annotations

from typing import Any

from ex_autoslot import ProfilableAutoSlots


# noinspection PyUnusedFunction
class JsonLibraryShim(ProfilableAutoSlots):
    def loads(self, json_str: str) -> dict[str, Any]: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter, reportExplicitAny]
    def dumps(self, object_dict: dict[str, Any], indent: int | None = None) -> str: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter, reportExplicitAny]
