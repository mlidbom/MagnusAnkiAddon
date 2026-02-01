from __future__ import annotations

import os
from typing import TYPE_CHECKING

import mylog
from dotnet import dotnet_runtime_loader
from testutils import ex_pytest
from typed_linq_collections.collections.q_set import QSet

is_testing = ex_pytest.is_testing

if TYPE_CHECKING:
    from collections.abc import Callable

    from configuration.configuration_value import JapaneseConfig
    from note.collection.jp_collection import JPCollection

_collection: JPCollection | None = None

_init_hooks: QSet[Callable[[], None]] = QSet()

def _call_init_hooks() -> None:
    global _init_hooks
    for hook in _init_hooks: hook()

def add_init_hook(hook: Callable[[], None]) -> None:
    _init_hooks.add(hook)

def config() -> JapaneseConfig:
    from configuration import configuration_value
    return configuration_value.config()

def _init(delay_seconds: float = 1.0) -> None:
    mylog.info(f"_init delay= {delay_seconds}")

    from note.collection.jp_collection import JPCollection
    global _collection
    if _collection is not None:
        _collection.reshchedule_init_for(delay_seconds)

    _collection = JPCollection(delay_seconds)
    _call_init_hooks()

def is_initialized() -> bool:
    return _collection is not None and _collection.is_initialized

def reset(delay_seconds: float = 0) -> None:
    mylog.info(f"reset: delay= {delay_seconds}")
    _destruct()
    _init(delay_seconds)

def _destruct() -> None:
    mylog.info("_destruct_ja_app")
    from sysutils.timeutil import StopWatch
    with StopWatch.log_warning_if_slower_than(0.2):
        global _collection
        if _collection is not None:
            _collection.destruct_sync()

        _collection = None

def col() -> JPCollection:
    if _collection is None: raise AssertionError("Collection not initialized")
    return _collection



user_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\\user_files")

dotnet_runtime_loader.ensure_clr_loaded()