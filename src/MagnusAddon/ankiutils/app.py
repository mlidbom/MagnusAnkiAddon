import gc
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Optional

from anki.collection import Collection
from anki.dbproxy import DBProxy
from anki.scheduler.v3 import Scheduler
from aqt import gui_hooks, mw, AnkiQt  # type: ignore

from ankiutils.ui_utils import UIUtils
from ankiutils.ui_utils_interface import IUIUtils
from note.collection.jp_collection import JPCollection
from sysutils.lazy import BackgroundInitialingLazy
from sysutils.typed import checked_cast


_collection:Optional[BackgroundInitialingLazy[JPCollection]] = None

def _reset(_anki_collection: Collection) -> None:
    global _collection
    if _collection:
        _collection.instance().destruct()
        gc.collect()

    _collection = BackgroundInitialingLazy(lambda: JPCollection(_anki_collection))

def reset() -> None:
    _reset(mw.col)

gui_hooks.collection_did_temporarily_close.append(_reset)
gui_hooks.collection_did_load.append(_reset)
gui_hooks.sync_did_finish.append(reset)

thread_pool_executor = ThreadPoolExecutor()
def ensure_initialized() -> None:
    col() #If the first call to this happens on a background threads things go south.

def col() -> JPCollection:
    assert _collection
    return _collection.instance()

def anki_collection() -> Collection: return col().anki_collection
def anki_db() -> DBProxy: return checked_cast(DBProxy, col().anki_collection.db)
def anki_scheduler() -> Scheduler: return checked_cast(Scheduler, col().anki_collection.sched)
def main_window() -> AnkiQt: return checked_cast(AnkiQt, mw)
def ui_utils() -> IUIUtils: return UIUtils(main_window())