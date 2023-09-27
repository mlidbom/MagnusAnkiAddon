from anki.collection import Collection
from aqt import mw


def get_anki_collection() -> Collection:
    return mw.col