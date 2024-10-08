import gc
from typing import cast

from anki.collection import Collection
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
    _reset2()

def _reset2() -> None:
    global _collection
    if _collection.is_initialized():
        _collection.instance().destruct()
        gc.collect()

    _collection = Lazy(lambda: JPCollection(cast(AnkiQt,mw).col))


gui_hooks.collection_did_load.append(_reset1)
gui_hooks.sync_did_finish.append(_reset2)

def col() -> JPCollection: return _collection.instance()
def anki_collection() -> Collection: return col().anki_collection
def main_window() -> AnkiQt: return checked_cast(AnkiQt, mw)
def ui_utils() -> IUIUtils: return UIUtils(main_window())