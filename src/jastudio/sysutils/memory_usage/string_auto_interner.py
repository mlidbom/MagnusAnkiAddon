from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from jastudio.ankiutils import app
from typed_linq_collections.collections.string_interning import set_default_intern_func

if TYPE_CHECKING:
    from typed_linq_collections.collections.q_list import QList

use_sys_intern = False

_is_enabled = False

def try_enable() -> None:  # call this after populating the application memory cache, thus discarding the unhelpful strings from interning and ensuring that the helpful ones stay using a single instance.
    global _is_enabled
    _is_enabled = app.config().enable_auto_string_interning.get_value()
    _env_override = os.environ.get("STRING_INTERNING")
    if _env_override:
        _is_enabled = _env_override == "1"

try_enable()

if use_sys_intern:  # noqa: SIM114
    def auto_intern(string: str) -> str:  # replace every string placed in any memory cache in the application with the value returned by this function
        # if not _is_enabled: return string
        return sys.intern(string)

    def auto_intern_list(strings: list[str]) -> list[str]:
        # if _is_enabled:
        for index, value in enumerate(strings):
            strings[index] = sys.intern(value)

        return strings

    def auto_intern_qlist(strings: QList[str]) -> QList[str]:
        # if _is_enabled:
        for index, value in enumerate(strings):
            strings[index] = sys.intern(value)

        return strings

else:
    simple_store = dict[str, str]()
    def auto_intern(string: str) -> str:  # replace every string placed in any memory cache in the application with the value returned by this function
        # if not _is_enabled: return string
        return simple_store.setdefault(string, string)

    def auto_intern_list(strings: list[str]) -> list[str]:
        # if _is_enabled:
        for index, value in enumerate(strings):
            strings[index] = simple_store.setdefault(value, value)

        return strings

    def auto_intern_qlist(strings: QList[str]) -> QList[str]:
        # if _is_enabled:
        for index, value in enumerate(strings):
            strings[index] = simple_store.setdefault(value, value)

        return strings

set_default_intern_func(auto_intern)
