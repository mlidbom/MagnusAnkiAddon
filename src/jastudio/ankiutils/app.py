from __future__ import annotations

import os
from typing import TYPE_CHECKING

import mylog
from sysutils.typed import checked_cast, non_optional
from testutils import ex_pytest
from typed_linq_collections.collections.q_set import QSet

is_testing = ex_pytest.is_testing

if TYPE_CHECKING:
    from collections.abc import Callable

    from anki.collection import Collection
    from anki.dbproxy import DBProxy
    from anki.scheduler.v3 import Scheduler  # pyright: ignore[reportMissingTypeStubs]
    from anki_extentions.config_manager_ex import ConfigManagerEx
    from ankiutils.ui_utils_interface import IUIUtils
    from aqt import AnkiQt  # type: ignore[attr-defined]  # pyright: ignore[reportPrivateImportUsage]
    from configuration.configuration_value import JapaneseConfig
    from note.collection.jp_collection import JPCollection

_collection: JPCollection | None = None

_init_hooks: QSet[Callable[[], None]] = QSet()
_collection_closed_hooks: QSet[Callable[[], None]] = QSet()

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

    from aqt import mw
    from note.collection.jp_collection import JPCollection
    global _collection
    if _collection is not None:
        _collection.reshchedule_init_for(delay_seconds)

    _collection = JPCollection(non_optional(mw.col), delay_seconds)
    _call_init_hooks()

def is_initialized() -> bool:
    return _collection is not None and _collection.is_initialized

def reset(delay_seconds: float = 0) -> None:
    mylog.info(f"reset: delay= {delay_seconds}")
    _destruct()
    _init(delay_seconds)

# noinspection Annotator
def _reset(_col: object | None = None) -> None:
    mylog.info("_reset")
    reset()

def _destruct() -> None:
    mylog.info("_destruct_ja_app")
    from sysutils.timeutil import StopWatch
    with StopWatch.log_warning_if_slower_than(0.2):
        global _collection
        if _collection is not None:
            _collection.destruct_sync()

        _collection = None

# noinspection Annotator
def _collection_is_being_invalidated(_col: object | None = None) -> None:
    mylog.info("_collection_is_being_invalidated")
    _destruct()
    reset(delay_seconds=9999)  # Unless forced by the user we don't actually want to run an initialization here

def _profile_closing() -> None:
    mylog.info("anki_profile_closing")
    from aqt import gui_hooks
    gui_hooks.sync_will_start.remove(_collection_is_being_invalidated)
    _collection_closed_hooks.remove(_destruct)
    gui_hooks.sync_did_finish.remove(_init)
    gui_hooks.collection_did_load.remove(_reset)  # pyright: ignore[reportUnknownMemberType]
    _destruct()

def _profile_opened() -> None:
    mylog.info("profile_opened")
    from aqt import gui_hooks
    gui_hooks.sync_will_start.append(_collection_is_being_invalidated)
    _collection_closed_hooks.add(_destruct)
    gui_hooks.sync_did_finish.append(_init)
    gui_hooks.collection_did_load.append(_reset)  # pyright: ignore[reportUnknownMemberType]
    _init(delay_seconds=1.0)

def anki_config() -> ConfigManagerEx:
    from anki_extentions.config_manager_ex import ConfigManagerEx
    from aqt import mw
    return ConfigManagerEx(non_optional(mw.col).conf)

def col() -> JPCollection:
    if _collection is None: raise AssertionError("Collection not initialized")
    return _collection

def anki_collection() -> Collection: return col().anki_collection

def anki_db() -> DBProxy: return non_optional(col().anki_collection.db)

def anki_scheduler() -> Scheduler:
    from anki.scheduler.v3 import Scheduler  # pyright: ignore[reportMissingTypeStubs]
    return checked_cast(Scheduler, col().anki_collection.sched)

def main_window() -> AnkiQt:
    from aqt import mw
    return non_optional(mw)

def get_ui_utils() -> IUIUtils:
    from ankiutils.ui_utils import UIUtils
    return UIUtils(main_window())

# noinspection Annotator
def _collection_closed(_collection: Collection, _downgrade: bool = False) -> None:
    for hook in _collection_closed_hooks:
        hook()

def _wrap_collection_close() -> None:
    import anki
    from anki.collection import Collection
    Collection.close = anki.hooks.wrap(Collection.close, _collection_closed, "before")  # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

_wrap_collection_close()

def _setup_gui_hooks() -> None:
    from aqt import gui_hooks
    gui_hooks.profile_will_close.append(_profile_closing)
    gui_hooks.profile_did_open.append(_profile_opened)

user_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\\user_files")

_setup_gui_hooks()
