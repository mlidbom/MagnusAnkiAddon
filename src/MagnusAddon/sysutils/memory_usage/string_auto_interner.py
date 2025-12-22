from __future__ import annotations

import sys

import mylog
from ankiutils import app
from typed_linq_collections.collections.q_dict import QDict
from typed_linq_collections.collections.string_interning import set_default_intern_func

_is_enabled = app.config().enable_auto_string_interning.get_value()

intern_hit_count = 0
intern_miss_count = 0

class StringWithUsage:
    def __init__(self, string: str) -> None:
        self.value: str = string
        self.usage_count: int = 1

    def is_worth_interning(self) -> bool:
        return self.usage_count > 100  # todo: should probably be some combination of length and usage count in the end

    def increment_usage_count(self) -> None:
        global intern_hit_count, intern_miss_count
        self.usage_count += 1
        if self.is_worth_interning():
            original_id = id(self.value)
            self.value = sys.intern(self.value)
            if id(self.value) == original_id:
                intern_hit_count += 1
            else:
                intern_miss_count += 1
            store.remove(self.value)
            interned_hashes.add(hash(self.value))

store = QDict[str, StringWithUsage]()


interned_hashes: set[int] = set()

def auto_intern(string: str) -> str:  # replace every string placed in any memory cache in the application with the value returned by this function
    if not _is_enabled: return string
    if hash(string) in interned_hashes: return sys.intern(string)

    value = store.get_or_add(string, StringWithUsage)
    value.increment_usage_count()
    return value.value


def auto_intern_list(strings: list[str]) -> None:
    if not _is_enabled: return
    for index, value in enumerate(strings):
        strings[index] = auto_intern(value)

def flush_store() -> None:  # call this after populating the application memory cache, thus discarding the unhelpful strings from interning and ensuring that the helpful ones stay using a single instance.
    non_interned = store.qcount()
    store.clear()
    mylog.info(f"string_auto_interner: interned {len(interned_hashes)} strings, removed {non_interned}: hit_count={intern_hit_count}, miss_count={intern_miss_count}")

set_default_intern_func(auto_intern)
