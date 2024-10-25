import gc

from anki.collection import Collection
from anki.dbproxy import DBProxy
from anki.scheduler.v3 import Scheduler
from aqt import gui_hooks, mw, AnkiQt  # type: ignore

from ankiutils.ui_utils import UIUtils
from ankiutils.ui_utils_interface import IUIUtils
from note.collection.jp_collection import JPCollection
from sysutils.lazy import Lazy
from sysutils.typed import checked_cast


def _always_failing_init() -> JPCollection:
    raise Exception("should never be called")

_collection:Lazy[JPCollection] = Lazy(_always_failing_init)
def _reset1(_collection: Collection) -> None:
    reset()

def reset() -> None:
    global _collection
    if _collection.is_initialized():
        _collection.instance().destruct()
        gc.collect()

    _collection = Lazy(lambda: JPCollection(checked_cast(AnkiQt,mw).col))


gui_hooks.collection_will_temporarily_close.append(_reset1)
gui_hooks.collection_did_temporarily_close.append(_reset1)
gui_hooks.profile_will_close.append(reset)
gui_hooks.collection_did_load.append(_reset1)
gui_hooks.sync_did_finish.append(reset)

def col() -> JPCollection: return _collection.instance()
def anki_collection() -> Collection: return col().anki_collection
def anki_db() -> DBProxy: return checked_cast(DBProxy, col().anki_collection.db)
def anki_scheduler() -> Scheduler: return checked_cast(Scheduler, col().anki_collection.sched)
def main_window() -> AnkiQt: return checked_cast(AnkiQt, mw)
def ui_utils() -> IUIUtils: return UIUtils(main_window())