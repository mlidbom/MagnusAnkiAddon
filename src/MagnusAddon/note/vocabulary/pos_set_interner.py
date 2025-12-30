from __future__ import annotations

from typing import TYPE_CHECKING

import mylog
from sysutils import ex_str
from sysutils.memory_usage import string_auto_interner
from typed_linq_collections.collections.q_dict import QDict
from typed_linq_collections.collections.q_frozen_set import QFrozenSet

if TYPE_CHECKING:
    from typed_linq_collections.collections.q_set import QSet

class POSSetManager:
    _pos_by_str: QDict[str, QFrozenSet[str]] = QDict()

    _remappings: QDict[str, str] = QDict({"intransitive verb": "intransitive",
                                          "transitive verb": "transitive",
                                          "godan": "godan verb",
                                          "な adjective": "na-adjective",
                                          "ichidan": "ichidan verb"})

    @staticmethod
    def _harmonize(pos: QSet[str]) -> QSet[str]:
        return pos.select(lambda it: POSSetManager._remappings.get(it, it)).to_set()

    @staticmethod
    def intern_and_harmonize(pos: str) -> str:
        if pos not in POSSetManager._pos_by_str:
            pos_values_set = ex_str.extract_comma_separated_values(pos).select(lambda it: it.lower()).to_set()
            pos_values_set = POSSetManager._harmonize(pos_values_set)
            pos = ", ".join(pos_values_set.order_by(lambda x: x))
            if pos not in POSSetManager._pos_by_str:
                POSSetManager._pos_by_str[string_auto_interner.auto_intern(pos)] = QFrozenSet(string_auto_interner.auto_intern_list(pos_values_set.to_list()))

        return pos

    @staticmethod
    def get(pos: str) -> QFrozenSet[str]: return POSSetManager._pos_by_str[pos]

    @staticmethod
    def log_stats() -> None:
        mylog.info(f"pos_set_interner: {len(POSSetManager._pos_by_str)} unique tag sets")
