from anki.collection import Collection
from aqt import mw

class Facade:
    def col(self) -> Collection: # noqa
        return mw.col

facade = Facade()