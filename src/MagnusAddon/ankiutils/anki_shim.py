from anki.collection import Collection
from aqt import mw

class Facade:
    def __init__(self) -> None:
        self._anki_collection = mw.col

    def anki_collection(self) -> Collection:
        return self._anki_collection

facade: Facade = Facade()