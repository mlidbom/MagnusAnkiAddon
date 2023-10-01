from anki.collection import Collection
from aqt import mw

class Facade:
    # noinspection PyMethodMayBeStatic
    def anki_collection(self) -> Collection: return mw.col

facade: Facade = Facade()