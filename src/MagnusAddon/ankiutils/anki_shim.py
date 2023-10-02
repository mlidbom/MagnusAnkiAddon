from anki.collection import Collection
from aqt import mw, AnkiQt

from sysutils.typed import checked_cast


class Facade:
    # noinspection PyMethodMayBeStatic
    def anki_collection(self) -> Collection: return mw.col  # type: ignore

    # noinspection PyMethodMayBeStatic
    def main_window(self) -> AnkiQt: return checked_cast(AnkiQt, mw)


facade: Facade = Facade()