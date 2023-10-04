from anki.collection import Collection
from aqt import mw, AnkiQt  # type: ignore

from ankiutils.ui_utils import UIUtils
from ankiutils.ui_utils_interface import UIUtilsInterface
from note.collection.jp_collection import JPCollection
from sysutils.lazy import Lazy
from sysutils.typed import checked_cast


_collection = Lazy(lambda: JPCollection(mw.col))  # type: ignore

def col() -> JPCollection: return _collection.instance()
def anki_collection() -> Collection: return col().anki_collection
def main_window() -> AnkiQt: return checked_cast(AnkiQt, mw)
def ui_utils() -> UIUtilsInterface: return UIUtils(main_window())