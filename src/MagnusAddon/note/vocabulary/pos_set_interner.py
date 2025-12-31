from __future__ import annotations

import mylog
from sysutils import ex_str
from sysutils.memory_usage import string_auto_interner
from typed_linq_collections.collections.q_dict import QDict


class POSSetManager:
    _pos_by_str: QDict[str, frozenset[str]] = QDict()

    _remappings: QDict[str, str] = QDict({"intransitive verb": "intransitive",
                                          "transitive verb": "transitive",
                                          "godan": "godan verb",
                                          "ichidan": "ichidan verb"})

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

    @staticmethod
    def log_stats() -> None:
        mylog.info(f"pos_set_interner: {len(POSSetManager._pos_by_str)} unique tag sets")
