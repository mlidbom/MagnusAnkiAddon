from __future__ import annotations

from sysutils import ex_str
from sysutils.memory_usage import string_auto_interner


class POSSetManager:
    _pos_by_str: dict[str, frozenset[str]] = {}

    _remappings: dict[str, str] = {"intransitive verb": "intransitive",
                                   "transitive verb": "transitive",
                                   "godan": "godan verb",
                                   "ichidan": "ichidan verb"}

    @staticmethod
    def _harmonize(pos: set[str]) -> set[str]:
        return {POSSetManager._remappings.get(it, it) for it in pos}

    @staticmethod
    def intern_and_harmonize(pos: str) -> str:
        if pos not in POSSetManager._pos_by_str:
            pos_values_set = ex_str.extract_comma_separated_values(pos).select(lambda it: it.lower()).to_set()
            pos_values_set = POSSetManager._harmonize(pos_values_set)
            pos = ", ".join(sorted(pos_values_set))
            if pos not in POSSetManager._pos_by_str:
                POSSetManager._pos_by_str[string_auto_interner.auto_intern(pos)] = frozenset(string_auto_interner.auto_intern_list(list(pos_values_set)))

        return pos

    @staticmethod
    def get(pos: str) -> frozenset[str]: return POSSetManager._pos_by_str[pos]
