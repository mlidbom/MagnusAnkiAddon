from __future__ import annotations

from anki.decks import DeckDict, DeckId
from anki_extentions.deck_configdict_ex import DeckConfigDictEx
from ankiutils import app
from sysutils.typed import checked_cast_generics, str_


class DeckEx:
    def __init__(self, deck_dict: DeckDict) -> None:
        self.deck_dict = deck_dict
        self.name = str_(deck_dict["name"])
        self.id = checked_cast_generics(DeckId, deck_dict["id"])


    def get_config(self) -> DeckConfigDictEx:
        return DeckConfigDictEx(app.anki_collection().decks.config_dict_for_deck_id(self.id))