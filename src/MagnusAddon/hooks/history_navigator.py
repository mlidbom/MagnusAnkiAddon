from anki.cards import Card, CardId
from aqt import mw, gui_hooks
from aqt.browser import Browser  # type: ignore
from aqt.qt import QKeySequence, QShortcut
from typing import List

from PyQt6.QtWidgets import QWidget

from ankiutils import query_builder, search_executor

class CardHistoryNavigator:
    def __init__(self) -> None:
        self.card_history: List[CardId] = []  # Stores card IDs
        self.current_position: int = -1

        gui_hooks.card_will_show.append(self.on_card_shown)  # Hook into card display

        def bind_shortcuts(widget: QWidget) -> None:
            self._reset_position()
            QShortcut(QKeySequence("Alt+Left"), widget).activated.connect(self.navigate_back)
            QShortcut(QKeySequence("Alt+Right"), widget).activated.connect(self.navigate_forward)

        bind_shortcuts(mw)
        gui_hooks.previewer_did_init.append(bind_shortcuts)
        gui_hooks.browser_will_show.append(bind_shortcuts)

        self.is_navigating: bool = False

    def _reset_position(self) -> None: self.current_position = len(self.card_history) - 1

    def on_card_shown(self, html: str, card: Card, _: str) -> str:
        if self.is_navigating:
            self.is_navigating = False
            return html

        if self.card_history and card.id == self.card_history[-1]: return html

        self.card_history.append(card.id)
        self._reset_position()

        return html

    def navigate_back(self) -> None:
        if self.current_position <= 0:
            return

        self.current_position -= 1
        self.is_navigating = True
        self._show_card_by_id(self.card_history[self.current_position])

    def navigate_forward(self) -> None:
        if self.current_position >= len(self.card_history) - 1:
            return

        self.current_position += 1
        self.is_navigating = True
        self._show_card_by_id(self.card_history[self.current_position])

    @staticmethod
    def _show_card_by_id(card_id: CardId) -> None:
        card = mw.col.get_card(card_id)
        search_executor.do_lookup(query_builder.open_card(card))

def init() -> None:
    CardHistoryNavigator()
