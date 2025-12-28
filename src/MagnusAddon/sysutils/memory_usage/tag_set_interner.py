from __future__ import annotations

import mylog
from sysutils.memory_usage import string_auto_interner
from typed_linq_collections.collections.q_set import QSet


class TagSetInterner:
    def __init__(self) -> None:
        self._tag_sets: dict[frozenset[str], tuple[QSet[str], list[str]]] = {}

    def intern(self, tags: list[str]) -> tuple[QSet[str], list[str]]:
        string_auto_interner.auto_intern_list(tags)

        key = frozenset(tags)
        if key not in self._tag_sets:
            self._tag_sets[key] = (QSet(tags), list(tags))

        return self._tag_sets[key]

    def log_stats(self) -> None:
        mylog.info(f"tag_set_interner: {len(self._tag_sets)} unique tag sets")

# Global singleton instance
tag_set_interner = TagSetInterner()
