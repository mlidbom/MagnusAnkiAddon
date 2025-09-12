from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from aqt import dialogs, mw
from aqt.browser import Browser  # pyright: ignore[reportPrivateImportUsage]
from note.cardutils import CardUtils
from sysutils import typed

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.cards import CardId

def refresh_search() -> None:
    browser: Browser = typed.checked_cast(Browser, dialogs.open("Browser", mw))  # pyright: ignore[reportAny]
    browser.onSearchActivated()

def prioritize_selected_cards(card_ids: Sequence[CardId]) -> None:
    cards = [app.anki_collection().get_card(card_id) for card_id in card_ids]
    for card in cards:
        CardUtils.prioritize(card)

    refresh_search()
