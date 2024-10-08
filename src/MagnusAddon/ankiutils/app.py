import gc
from typing import cast

from anki.collection import Collection
from aqt import gui_hooks, mw, AnkiQt  # type: ignore

from ankiutils.ui_utils import UIUtils
from ankiutils.ui_utils_interface import IUIUtils
from note.collection.jp_collection import JPCollection
from sysutils.lazy import Lazy
from sysutils.typed import checked_cast


_collection:Lazy[JPCollection]
def _init_collection(collection: Collection) -> None:
    global _collection
    _collection = Lazy(lambda: JPCollection(collection))

def _reset() -> None:
    global _collection
    if _collection.is_initialized():
        _collection.instance().destruct()

    gc.collect()
    _collection = Lazy(lambda: JPCollection(cast(Collection, mw.col)))


gui_hooks.collection_did_load.append(_init_collection)
gui_hooks.sync_did_finish.append(_reset)

def col() -> JPCollection: return _collection.instance()
def anki_collection() -> Collection: return col().anki_collection
def main_window() -> AnkiQt: return checked_cast(AnkiQt, mw)
def ui_utils() -> IUIUtils: return UIUtils(main_window())