from anki.cards import Card, CardId
from aqt import mw, gui_hooks
from aqt.browser import Browser  # type: ignore
from aqt.qt import QKeySequence, QShortcut
from typing import List
import json
import os

from PyQt6.QtWidgets import QWidget

from ankiutils import query_builder, search_executor
from sysutils import typed

class CardHistoryNavigator:
    def __init__(self) -> None:
        self.card_history: List[CardId] = []  # Stores card IDs
        self.current_position: int = -1

        # Load history from file
        self._load_history_from_file()

        gui_hooks.card_will_show.append(self.on_card_shown)  # Hook into card display

        def bind_shortcuts(widget: QWidget) -> None:
            self._reset_position()
            QShortcut(QKeySequence("Alt+Left"), widget).activated.connect(self.navigate_back)
            QShortcut(QKeySequence("Alt+Right"), widget).activated.connect(self.navigate_forward)

        bind_shortcuts(mw)
        gui_hooks.previewer_did_init.append(bind_shortcuts)
        gui_hooks.browser_will_show.append(bind_shortcuts)

        self.is_navigating: bool = False

    def _reset_position(self) -> None:
        self.current_position = len(self.card_history) - 1

    @staticmethod
    def _get_history_file_path() -> str:
        addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(addon_dir, "card_history.json")

    def _save_last_hundred_items_to_file(self) -> None:
        history_file_path = self._get_history_file_path()
        last_hundred_items = [int(card_id) for card_id in self.card_history[-100:]]

        with open(history_file_path, "w") as history_file:
            json.dump(last_hundred_items, history_file)

    def _load_history_from_file(self) -> None:
        history_file_path = self._get_history_file_path()

        if os.path.exists(history_file_path):
            with open(history_file_path, "r") as history_file:
                saved_history = typed.checked_cast_generics(list[int], json.load(history_file))
                self.card_history = [CardId(card_id) for card_id in saved_history]
                self._reset_position()

    def on_card_shown(self, html: str, card: Card, _: str) -> str:
        if self.is_navigating:
            self.is_navigating = False
            return html

        if self.card_history and card.id == self.card_history[-1]: return html

        if card.id in self.card_history:
            self.card_history.remove(card.id)

        self.card_history.append(card.id)
        self._reset_position()

        # Save history to file
        self._save_last_hundred_items_to_file()

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