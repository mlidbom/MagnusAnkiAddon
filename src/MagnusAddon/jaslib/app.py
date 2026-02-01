from __future__ import annotations

import os
from typing import TYPE_CHECKING

from jaslib.dotnet import dotnet_runtime_loader
from jaslib.testutils import ex_pytest
from typed_linq_collections.collections.q_set import QSet

is_testing = ex_pytest.is_testing

if TYPE_CHECKING:
    from collections.abc import Callable

    from jaslib.configuration.configuration_value import JapaneseConfig
    from jaslib.note.collection.jp_collection import JPCollection

_collection: JPCollection | None = None

_init_hooks: QSet[Callable[[], None]] = QSet()

def add_init_hook(hook: Callable[[], None]) -> None:
    _init_hooks.add(hook) # todo migration

def config() -> JapaneseConfig:
    from jaslib.configuration import configuration_value
    return configuration_value.config()

def col() -> JPCollection:
    if _collection is None: raise AssertionError("Collection not initialized")
    return _collection

user_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_files")

dotnet_runtime_loader.ensure_clr_loaded()