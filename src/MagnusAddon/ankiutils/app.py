import gc
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
    _destruct()

    _collection = BackgroundInitialingLazy(lambda: JPCollection(_anki_collection))

def _destruct(_: Optional[Collection] = None) ->None:
    global _collection
    if _collection:
        _collection.instance().destruct()
        _collection = None
        gc.collect()

def reset() -> None:
    _reset(mw.col)

gui_hooks.collection_will_temporarily_close.append(_destruct)
gui_hooks.profile_will_close.append(_destruct)

gui_hooks.collection_did_temporarily_close.append(_reset)
gui_hooks.collection_did_load.append(_reset)
gui_hooks.sync_did_finish.append(reset)

def col() -> JPCollection:
    assert _collection
    return _collection.instance()

def anki_collection() -> Collection: return col().anki_collection
def anki_db() -> DBProxy: return checked_cast(DBProxy, col().anki_collection.db)
def anki_scheduler() -> Scheduler: return checked_cast(Scheduler, col().anki_collection.sched)
def main_window() -> AnkiQt: return checked_cast(AnkiQt, mw)
def ui_utils() -> IUIUtils: return UIUtils(main_window())