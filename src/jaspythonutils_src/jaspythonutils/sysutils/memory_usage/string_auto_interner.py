from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from JAStudio.Core import App
from typed_linq_collections.collections.q_dict import QDict
from typed_linq_collections.collections.string_interning import set_default_intern_func

if TYPE_CHECKING:
    from typed_linq_collections.collections.q_list import QList

use_sys_intern = False
use_simple_interner = True

_is_enabled = False

def try_enable() -> None:  # call this after populating the application memory cache, thus discarding the unhelpful strings from interning and ensuring that the helpful ones stay using a single instance.
    global _is_enabled
    _is_enabled = App.Config().EnableAutoStringInterning.GetValue()
    _env_override = os.environ.get("STRING_INTERNING")
    if _env_override:
        _is_enabled = _env_override == "1"

try_enable()

if use_sys_intern:  # noqa: SIM114
    def auto_intern(string: str) -> str:  # replace every string placed in any memory cache in the application with the value returned by this function
        #if not _is_enabled: return string
        return sys.intern(string)

    def auto_intern_list(strings: list[str]) -> list[str]:
        #if _is_enabled:
        for index, value in enumerate(strings):
            strings[index] = sys.intern(value)

        return strings

    def auto_intern_qlist(strings: QList[str]) -> QList[str]:
        #if _is_enabled:
        for index, value in enumerate(strings):
            strings[index] = sys.intern(value)

        return strings

elif use_simple_interner:
    simple_store = dict[str, str]()
    def auto_intern(string: str) -> str:  # replace every string placed in any memory cache in the application with the value returned by this function
        #if not _is_enabled: return string
        return simple_store.setdefault(string, string)

    def auto_intern_list(strings: list[str]) -> list[str]:
        #if _is_enabled:
        for index, value in enumerate(strings):
            strings[index] = simple_store.setdefault(value, value)

        return strings

    def auto_intern_qlist(strings: QList[str]) -> QList[str]:
        #if _is_enabled:
        for index, value in enumerate(strings):
            strings[index] = simple_store.setdefault(value, value)

        return strings
else:
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

    def auto_intern_list(strings: list[str]) -> list[str]:
        if _is_enabled:
            for index, value in enumerate(strings):
                strings[index] = auto_intern(value)
        return strings

set_default_intern_func(auto_intern)
