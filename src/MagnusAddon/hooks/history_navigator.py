from anki.cards import Card, CardId
from aqt import mw, gui_hooks
from aqt.browser import Browser  # type: ignore
from aqt.browser.previewer import BrowserPreviewer
from aqt.qt import QKeySequence, QShortcut
from typing import Any, List

from ankiutils import query_builder, search_executor
from sysutils import typed

class CardHistoryNavigator:
    def __init__(self) -> None:
        self.card_history: List[CardId] = []  # Stores card IDs
        self.current_position: int = -1

        self.back_shortcut = QShortcut(QKeySequence("Alt+Left"), mw)
        self.back_shortcut.activated.connect(self.navigate_back)
        self.forward_shortcut = QShortcut(QKeySequence("Alt+Right"), mw)
        self.forward_shortcut.activated.connect(self.navigate_forward)

        gui_hooks.card_will_show.append(self.on_card_shown)# Hook into card display

        self.is_navigating:bool = False

    def on_card_shown(self, html: str, card:Card, context:Any) -> str:
        if not mw.state == "deckBrowser": return html

        if self.is_navigating:# If we're navigating through history, don't add the card again
            self.is_navigating = False
            return html

        if self.current_position == len(self.card_history) - 1: # If we're at the end of the history, append the new card
            self.card_history.append(card.id)
            self.current_position += 1
        else: # We're in the middle of history, truncate and add new card
            self.card_history = self.card_history[:self.current_position + 1]
            self.card_history.append(card.id)
            self.current_position += 1

        return html

    def navigate_back(self) -> None:
        if self.current_position <= 0 or not mw.state == "review":
            return

        self.current_position -= 1
        self.is_navigating = True
        self._show_card_by_id(self.card_history[self.current_position])

    def navigate_forward(self) -> None:
        if self.current_position >= len(self.card_history) - 1 or not mw.state == "review":
            return

        self.current_position += 1
        self.is_navigating = True
        self._show_card_by_id(self.card_history[self.current_position])

    @staticmethod
    def browser() -> Browser:
        browser = [window for window in mw.app.topLevelWidgets() if isinstance(window, Browser)]
        return typed.checked_cast(Browser, browser[0])

    def previewer(self) -> BrowserPreviewer:
        return typed.checked_cast(BrowserPreviewer, self.browser()._previewer) # noqa

    @staticmethod
    def _show_card_by_id(card_id: CardId) -> None:
        card = mw.col.get_card(card_id)
        search_executor.do_lookup(query_builder.open_card(card))

def init() -> None:
    CardHistoryNavigator()
