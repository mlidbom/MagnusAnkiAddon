from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from aqt import dialogs, mw
from note.cardutils import CardUtils

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.cards import CardId
    from aqt.browser import Browser  # type: ignore

def refresh_search() -> None:
    browser: Browser = dialogs.open("Browser", mw)
    browser.onSearchActivated()

def prioritize_selected_cards(card_ids: Sequence[CardId]) -> None:
    cards = [app.anki_collection().get_card(card_id) for card_id in card_ids]
    for card in cards:
        CardUtils.prioritize(card)

    refresh_search()
