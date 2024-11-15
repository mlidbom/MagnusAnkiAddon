from anki.decks import DeckDict

from sysutils.typed import str_

class DeckEx:
    def __init__(self, deck_dict: DeckDict) -> None:
        self.deck_dict = deck_dict

    def name(self) -> str: return str_(self.deck_dict['name'])