import gc
from typing import Optional
import threading

from anki.collection import Collection
from anki.dbproxy import DBProxy
from anki.scheduler.v3 import Scheduler
from aqt import gui_hooks, mw, AnkiQt  # type: ignore
from aqt import gui_hooks, mw

from ankiutils.ui_utils import UIUtils
from ankiutils.ui_utils_interface import IUIUtils
from note.collection.jp_collection import JPCollection
from sysutils.lazy import BackgroundInitialingLazy
from sysutils.typed import checked_cast

_collection: Optional[BackgroundInitialingLazy[JPCollection]] = None
_init_lock = threading.RLock()
_pending_init_timer: Optional[threading.Timer] = None

def _cancel_pending_init() -> None:
    global _pending_init_timer
    if _pending_init_timer:
        _pending_init_timer.cancel()
        _pending_init_timer = None

def _schedule_init() -> None:
    global _pending_init_timer
    _pending_init_timer = threading.Timer(1.0, lambda: _init())
    _pending_init_timer.start()

def _init() -> None:
    global _pending_init_timer, _collection
    with _init_lock:
        _cancel_pending_init()
        assert not _collection
        _collection = BackgroundInitialingLazy(lambda: JPCollection(mw.col))

def reset() -> None:
    _destruct()
    _init()

def _destruct() -> None:
    global _collection
    with _init_lock:
        _cancel_pending_init()

        if _collection:
            _collection.instance().destruct()
            _collection = None
            gc.collect()

gui_hooks.profile_will_close.append(_destruct)
gui_hooks.sync_will_start.append(_destruct)

gui_hooks.profile_did_open.append(_schedule_init)
gui_hooks.sync_did_finish.append(_init)

def col() -> JPCollection:
    assert _collection
    return _collection.instance()

def anki_collection() -> Collection: return col().anki_collection
def anki_db() -> DBProxy: return checked_cast(DBProxy, col().anki_collection.db)
def anki_scheduler() -> Scheduler: return checked_cast(Scheduler, col().anki_collection.sched)
def main_window() -> AnkiQt: return checked_cast(AnkiQt, mw)
def ui_utils() -> IUIUtils: return UIUtils(main_window())
