import gc
from typing import Optional

from anki.collection import Collection
from anki.dbproxy import DBProxy
from anki.scheduler.v3 import Scheduler
from aqt import gui_hooks, mw, AnkiQt  # type: ignore
from aqt import gui_hooks, mw

from ankiutils.ui_utils import UIUtils
from ankiutils.ui_utils_interface import IUIUtils
from configuration.configuration import JapaneseConfig
from note.collection.jp_collection import JPCollection
from sysutils.lazy import BackgroundInitialingLazy
from sysutils.typed import checked_cast

_collection: Optional[BackgroundInitialingLazy[JPCollection]] = None

config:JapaneseConfig = JapaneseConfig()

def _init(delay_seconds: float = 0) -> None:
    global _collection
    if _collection and not _collection.try_cancel_scheduled_init():
        return

    _collection = BackgroundInitialingLazy(lambda: JPCollection(mw.col), delay_seconds=delay_seconds)

def reset(delay_seconds: float = 0) -> None:
    _destruct()
    _init(delay_seconds)

def _destruct() -> None:
    global _collection
    if _collection and not _collection.try_cancel_scheduled_init():
        _collection.instance().destruct()
        _collection = None
        gc.collect()

def _sync_starting() -> None:
    reset(delay_seconds=9999) #Unless forced by the user we don't actually want to run an initialization here

def _profile_closing() -> None:
    gui_hooks.sync_will_start.remove(_sync_starting)
    gui_hooks.sync_did_finish.remove(_init)
    _destruct()

def _profile_opened() -> None:
    gui_hooks.sync_will_start.append(_sync_starting)
    gui_hooks.sync_did_finish.append(_init)
    _init(delay_seconds=1.0)

gui_hooks.profile_will_close.append(_profile_closing)
gui_hooks.profile_did_open.append(_profile_opened)

def wait_for_initialization() -> None:
    col()

def col() -> JPCollection:
    assert _collection
    return _collection.instance()

def anki_collection() -> Collection: return col().anki_collection
def anki_db() -> DBProxy: return checked_cast(DBProxy, col().anki_collection.db)
def anki_scheduler() -> Scheduler: return checked_cast(Scheduler, col().anki_collection.sched)
def main_window() -> AnkiQt: return checked_cast(AnkiQt, mw)
def ui_utils() -> IUIUtils: return UIUtils(main_window())
