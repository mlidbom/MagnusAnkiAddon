from __future__ import annotations
import gc
from typing import Any, Callable, Optional, TYPE_CHECKING

import anki

from anki_extentions.config_manager_ex import ConfigManagerEx
from sysutils.timeutil import StopWatch

if TYPE_CHECKING:
    from configuration.configuration import JapaneseConfig

from anki.collection import Collection
from anki.dbproxy import DBProxy
from anki.scheduler.v3 import Scheduler
from aqt import gui_hooks, mw, AnkiQt  # type: ignore
from aqt import gui_hooks, mw

from ankiutils.ui_utils import UIUtils
from ankiutils.ui_utils_interface import IUIUtils
from note.collection.jp_collection import JPCollection
from sysutils.lazy import BackgroundInitialingLazy
from sysutils.typed import checked_cast, non_optional



_collection: Optional[BackgroundInitialingLazy[JPCollection]] = None


_init_hooks: set[Callable[[], None]] = set()
_collection_closed_hooks: set[Callable[[], None]] = set()

def _call_init_hooks() -> None:
    global _init_hooks
    for hook in _init_hooks: hook()

def add_init_hook(hook:Callable[[], None]) -> None:
    _init_hooks.add(hook)

def config() -> JapaneseConfig:
    from configuration import configuration
    return configuration.config


def _init(_col:Optional[Any] = None, delay_seconds: float = 0) -> None:
    global _collection
    if _collection and not _collection.try_cancel_scheduled_init():
        return

    _collection = BackgroundInitialingLazy(lambda: JPCollection(mw.col), delay_seconds=delay_seconds)
    _call_init_hooks()

def reset(delay_seconds: float = 0) -> None:
    _destruct()
    _init(delay_seconds)

def _reset(_col:Optional[Any] = None) -> None:
    reset()

def _destruct() -> None:
    global _collection
    if _collection and not _collection.try_cancel_scheduled_init():
        _collection.instance().destruct()
        gc.collect()

    _collection = None

def _collection_is_being_invalidated(_col:Optional[Any] = None) -> None:
    _destruct()
    reset(delay_seconds=9999) #Unless forced by the user we don't actually want to run an initialization here

def _profile_closing() -> None:
    gui_hooks.sync_will_start.remove(_collection_is_being_invalidated)
    _collection_closed_hooks.remove(_destruct)
    gui_hooks.sync_did_finish.remove(_init)
    gui_hooks.collection_did_load.remove(_reset)
    _destruct()

def _profile_opened() -> None:
    gui_hooks.sync_will_start.append(_collection_is_being_invalidated)
    _collection_closed_hooks.add(_destruct)
    gui_hooks.sync_did_finish.append(_init)
    gui_hooks.collection_did_load.append(_reset)
    _init(delay_seconds=1.0)

def wait_for_initialization() -> None:
    with StopWatch.log_warning_if_slower_than("app.wait_for_initialization", 0.01):
        col()

def anki_config() -> ConfigManagerEx:
    return ConfigManagerEx(mw.col.conf)

def col() -> JPCollection:
    assert _collection
    return _collection.instance()

def anki_collection() -> Collection: return col().anki_collection
def anki_db() -> DBProxy: return non_optional(col().anki_collection.db)
def anki_scheduler() -> Scheduler: return checked_cast(Scheduler, col().anki_collection.sched)
def main_window() -> AnkiQt: return non_optional(mw)
def ui_utils() -> IUIUtils: return UIUtils(main_window())

def _collection_closed(_self: Collection, _downgrade: bool = False) -> None:
    for hook in _collection_closed_hooks:
        hook()

Collection.close = anki.hooks.wrap(Collection.close, _collection_closed, "before")  # type: ignore
gui_hooks.profile_will_close.append(_profile_closing)
gui_hooks.profile_did_open.append(_profile_opened)
