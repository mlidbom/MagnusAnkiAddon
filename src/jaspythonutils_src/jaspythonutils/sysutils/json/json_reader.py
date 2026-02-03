from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from autoslot import Slots  # pyright: ignore [reportMissingTypeStubs]
from jaspythonutils.sysutils import typed
from jaspythonutils.sysutils.json.ex_json import json_library_shim
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from collections.abc import Callable

    from jaspythonutils.sysutils.standard_type_aliases import Selector

class JsonReader(Slots):
    def __init__(self, json_dict: dict[str, Any]) -> None:  # pyright: ignore[reportExplicitAny]
        self._dict: dict[str, Any] = json_dict  # pyright: ignore[reportExplicitAny]

    def _get_prop(self, prop: str | list[str], default: object | None) -> Any:  # noqa: ANN401  # pyright: ignore[reportExplicitAny, reportAny]
        if isinstance(prop, str):
            value = self._dict.get(prop, None)
            if value is None:
                if default is not None: return default
                raise KeyError(f"Property '{prop}' not found in the JSON.")
            return value  # pyright: ignore[reportAny]

        for current_property_name in prop:
            if current_property_name in self._dict:
                return self._dict[current_property_name]  # pyright: ignore[reportAny]

        if default is not None: return default
        raise KeyError(f"None of the following keys were found in the JSON: {prop}")

    def string(self, prop: str | list[str], default: str | None = None) -> str: return cast(str, self._get_prop(prop, default))
    def integer(self, prop: str | list[str], default: int | None = None) -> int: return cast(int, self._get_prop(prop, default))

    def string_list(self, prop: str | list[str], default: list[str] | None = None) -> list[str]:
        return cast(list[str], self._get_prop(prop, default))

    def string_set(self, prop: str | list[str], default: list[str] | None = None) -> QSet[str]: return QSet(self.string_list(prop, default))

    def object_list[TProp](self, prop: str | list[str], factory: Selector[JsonReader, TProp], default: list[TProp] | None = None) -> list[TProp]:
        prop_value = cast(list[dict[str, Any]], self._get_prop(prop, default))  # pyright: ignore[reportExplicitAny]
        reader_list = [JsonReader(json_dict) for json_dict in prop_value]
        return [factory(reader) for reader in reader_list]

    # noinspection PyUnusedFunction
    def object[TProp](self, prop: str, factory: Selector[JsonReader, TProp], default: Callable[[], TProp] | None = None) -> TProp | None:
        reader = self._reader_or_none(prop)
        return default() if reader is None and default is not None else factory(typed.non_optional(reader))

    def _reader_or_none(self, prop: str) -> JsonReader | None:
        dict_ = self._dict.get(prop, None)
        return None if dict_ is None else JsonReader(cast(dict[str, Any], dict_))  # pyright: ignore[reportExplicitAny]

    @classmethod
    def from_json(cls, json_str: str) -> JsonReader:
        return cls(json_library_shim.loads(json_str))
