from anki.decks import DeckConfigDict
from sysutils.typed import *


class DeckConfigDictEx:
    def __init__(self, deck_config_dict:DeckConfigDict) -> None:
        self._dict = deck_config_dict

    def get_seconds_to_show_question(self) -> float:
        return float_(self._dict.get('secondsToShowQuestion'))