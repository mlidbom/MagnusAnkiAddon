from __future__ import annotations

from typing import cast

from anki.decks import DeckDict, DeckId
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

from jastudio.anki_extentions.deck_configdict_ex import DeckConfigDictEx
from jastudio.ankiutils import app
from jastudio.sysutils.typed import str_


class DeckEx(Slots):
    def __init__(self, deck_dict: DeckDict) -> None:
        self.deck_dict: DeckDict = deck_dict
        self.name: str = str_(deck_dict["name"])  # pyright: ignore[reportAny]
        self.id: DeckId = cast(DeckId, deck_dict["id"])

    def get_config(self) -> DeckConfigDictEx:
        return DeckConfigDictEx(app.anki_collection().decks.config_dict_for_deck_id(self.id))
