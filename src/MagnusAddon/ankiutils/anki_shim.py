from anki.collection import Collection
from aqt import mw, AnkiQt  # type: ignore

from ankiutils.ui_utils import UIUtils
from ankiutils.ui_utils_interface import UIUtilsInterface
from sysutils.typed import checked_cast

# noinspection PyMethodMayBeStatic
class Facade:
    def anki_collection(self) -> Collection: return mw.col  # type: ignore
    def main_window(self) -> AnkiQt: return checked_cast(AnkiQt, mw)
    def ui_utils(self) -> UIUtilsInterface: return UIUtils(self.main_window())


facade: Facade = Facade()