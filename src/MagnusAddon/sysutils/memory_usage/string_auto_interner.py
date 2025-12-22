from __future__ import annotations

import sys

from typed_linq_collections.collections.q_dict import QDict


class StringWithUsage:
    def __init__(self, string: str) -> None:
        self.value: str = string
        self.usage_count: int = 0

    def is_worth_interning(self) -> bool:
        return self.usage_count > 100  # todo: should probably be some combination of length and usage count in the end, but for new we intern everything

store = QDict[str, StringWithUsage]()

def auto_intern(string: str) -> str:  # replace every string placed in any memory cache in the application with the value returned by this function
    if string not in store:
        store[string] = StringWithUsage(string)

    return store[string].value

def flush_store() -> None:  # call this after populating the application memory cache, thus discarding the unhelpful strings from interning and ensuring that the helpful ones stay using a single instance.
    (store.qitems()
     .where(lambda it: it.value.is_worth_interning())
     .for_each(lambda it: sys.intern(it.value.value)))

    store.remove_where(lambda it: not it.value.is_worth_interning())

    store.clear()
