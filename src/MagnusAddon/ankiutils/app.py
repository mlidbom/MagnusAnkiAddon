from __future__ import annotations

import gc
from typing import TYPE_CHECKING, Callable, Optional

from sysutils.lazy import BackgroundInitialingLazy
from sysutils.typed import checked_cast, non_optional

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.dbproxy import DBProxy
    from anki.scheduler.v3 import Scheduler
    from anki_extentions.config_manager_ex import ConfigManagerEx
    from ankiutils.ui_utils_interface import IUIUtils
    from aqt import AnkiQt
    from configuration.configuration_value import JapaneseConfig
    from note.collection.jp_collection import JPCollection

_collection: Optional[BackgroundInitialingLazy[JPCollection]] = None


_init_hooks: set[Callable[[], None]] = set()
_collection_closed_hooks: set[Callable[[], None]] = set()

def _call_init_hooks() -> None:
    global _init_hooks
    for hook in _init_hooks: hook()

def add_init_hook(hook:Callable[[], None]) -> None:
    _init_hooks.add(hook)

def config() -> JapaneseConfig:
    from configuration import configuration_value
    return configuration_value.config.instance()


def _init(_col:Optional[object] = None, delay_seconds: float = 0) -> None:
    from aqt import mw
    from note.collection.jp_collection import JPCollection
    global _collection
    if _collection and not _collection.try_cancel_scheduled_init():
        return

    _collection = BackgroundInitialingLazy(lambda: JPCollection(mw.col), delay_seconds=delay_seconds)
    _call_init_hooks()

def is_initialized() -> bool:
    return _collection and _collection.is_initialized()

def reset(delay_seconds: float = 0) -> None:
    _destruct()
    _init(delay_seconds)

def is_testing() -> bool:
    import sys
    return "pytest" in sys.modules

def _reset(_col:Optional[object] = None) -> None:
    reset()

def _destruct() -> None:
    from sysutils.timeutil import StopWatch
    with StopWatch.log_warning_if_slower_than(0.2):
        global _collection
        if _collection and not _collection.try_cancel_scheduled_init():
            _collection.instance().destruct_async()

        _collection = None

def _collection_is_being_invalidated(_col:Optional[object] = None) -> None:
    _destruct()
    reset(delay_seconds=9999) #Unless forced by the user we don't actually want to run an initialization here

def _profile_closing() -> None:
    from aqt import gui_hooks
    gui_hooks.sync_will_start.remove(_collection_is_being_invalidated)
    _collection_closed_hooks.remove(_destruct)
    gui_hooks.sync_did_finish.remove(_init)
    gui_hooks.collection_did_load.remove(_reset)
    _destruct()

def _profile_opened() -> None:
    from aqt import gui_hooks
    gui_hooks.sync_will_start.append(_collection_is_being_invalidated)
    _collection_closed_hooks.add(_destruct)
    gui_hooks.sync_did_finish.append(_init)
    gui_hooks.collection_did_load.append(_reset)
    _init(delay_seconds=1.0)

def anki_config() -> ConfigManagerEx:
    from anki_extentions.config_manager_ex import ConfigManagerEx
    from aqt import mw
    return ConfigManagerEx(mw.col.conf)

def col() -> JPCollection:
    from sysutils.timeutil import StopWatch
    with StopWatch.log_warning_if_slower_than(0.01, "waiting_for_initialization"):
        assert _collection
        return _collection.instance()

def anki_collection() -> Collection: return col().anki_collection
def anki_db() -> DBProxy: return non_optional(col().anki_collection.db)
def anki_scheduler() -> Scheduler:
    from anki.scheduler.v3 import Scheduler
    return checked_cast(Scheduler, col().anki_collection.sched)

def main_window() -> AnkiQt:
    from aqt import mw
    return non_optional(mw)

def get_ui_utils() -> IUIUtils:
    from ankiutils.ui_utils import UIUtils
    return UIUtils(main_window())

def _collection_closed(_collection: Collection, _downgrade: bool = False) -> None:
    for hook in _collection_closed_hooks:
        hook()

def _wrap_collection_close() -> None:
    import anki
    from anki.collection import Collection
    Collection.close = anki.hooks.wrap(Collection.close, _collection_closed, "before")

_wrap_collection_close()

def _setup_gui_hooks() -> None:
    from aqt import gui_hooks
    gui_hooks.profile_will_close.append(_profile_closing)
    gui_hooks.profile_did_open.append(_profile_opened)

_setup_gui_hooks()

