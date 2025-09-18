from __future__ import annotations

from typing import TYPE_CHECKING

from ex_autoslot import AutoSlots
from sysutils.typed import float_

if TYPE_CHECKING:
    from anki.decks import DeckConfigDict


class DeckConfigDictEx(AutoSlots):
    def __init__(self, deck_config_dict:DeckConfigDict) -> None:
        self._dict:DeckConfigDict = deck_config_dict

    def get_seconds_to_show_question(self) -> float:
        return float_(self._dict.get("secondsToShowQuestion"))