from __future__ import annotations

import json
import os

from anki.cards import Card, CardId
from ankiutils import app, query_builder, search_executor, ui_utils
from aqt import gui_hooks, mw
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils import typed
from sysutils.typed import non_optional
from sysutils.weak_ref import WeakRefable


class CardHistoryNavigator(WeakRefable, Slots):
    def __init__(self) -> None:
        self.card_history: list[CardId] = []  # Stores card IDs
        self.current_position: int = -1

        self._load_history_from_file()

        self._is_navigating: bool = False
        self._last_card_shown_was_navigated_card_id: CardId | None = None
        self._last_card_shown_in_reviewer_card_id: CardId | None = None

    def _set_current_position_to_end_of_history(self) -> None:
        self.current_position = len(self.card_history) - 1

    @classmethod
    def _get_history_file_path(cls) -> str:
        return os.path.join(app.user_files_dir, "card_history.json")

    def _save_last_hundred_items_to_file(self) -> None:
        history_file_path = self._get_history_file_path()
        last_hundred_items = [int(card_id) for card_id in self.card_history[-100:]]

        with open(history_file_path, "w") as history_file:
            json.dump(last_hundred_items, history_file)

    def _load_history_from_file(self) -> None:
        history_file_path = self._get_history_file_path()

        if os.path.exists(history_file_path):
            with open(history_file_path) as history_file:
                saved_history = typed.checked_cast_generics(list[int], json.load(history_file))  # pyright: ignore[reportAny]
                self.card_history = [CardId(card_id) for card_id in saved_history]
                self._set_current_position_to_end_of_history()

    def on_card_shown(self, html: str, card_being_displayed: Card, _display_type: str) -> str:
        if ui_utils.is_reviewer_display_type(_display_type):
            if self._last_card_shown_in_reviewer_card_id == card_being_displayed.id: return html  # We don't want to pollute the history every single time the currently reviewed card is refreshed by our UI refresh code....
            self._last_card_shown_in_reviewer_card_id = card_being_displayed.id

        if self._is_navigating:  # don't mess up the history when navigating the history. Navigating the history is a read-only operation
            self._is_navigating = False
            self._last_card_shown_was_navigated_card_id = card_being_displayed.id
            return html
        else:
            # if we navigate away from a card shown while navigating the history, that was probably the card we were searching for and if we hit back after that, we want that card
            if self._last_card_shown_was_navigated_card_id is not None:
                self.move_to_front_of_history(self._last_card_shown_was_navigated_card_id)
                self._last_card_shown_was_navigated_card_id = None

            self.move_to_front_of_history(card_being_displayed.id)

            self._set_current_position_to_end_of_history()
            self._save_last_hundred_items_to_file()
            return html

    def move_to_front_of_history(self, card_id: CardId) -> None:
        while card_id in self.card_history: self.card_history.remove(card_id)  # no duplicates in the history please
        self.card_history.append(card_id)

    @classmethod
    def _card_exists(cls, card_id: CardId) -> bool:
        # noinspection PyBroadException
        try:
            _discarded = non_optional(mw.col).get_card(card_id)
            return True  # noqa: TRY300
        except:  # noqa: E722
            return False

    def navigate_back(self) -> None:
        if self._is_at_start_of_history():
            return

        self.current_position -= 1

        while self.current_position >= 0 and not self._card_exists(self.card_history[self.current_position]):
            self.current_position -= 1

        if self.current_position < 0:
            self.current_position = 0
            return

        self._is_navigating = True
        self._show_card_by_id(self.card_history[self.current_position])

    def navigate_forward(self) -> None:
        if self._is_at_end_of_history():
            return

        self.current_position += 1
        while self.current_position < len(self.card_history) and not self._card_exists(self.card_history[self.current_position]):
            self.current_position += 1

        if self.current_position >= len(self.card_history):
            self.current_position = len(self.card_history) - 1
            return

        self._is_navigating = True
        self._show_card_by_id(self.card_history[self.current_position])

    def _is_at_end_of_history(self) -> bool: return self.current_position >= len(self.card_history) - 1
    def _is_at_start_of_history(self) -> bool: return self.current_position <= 0

    @classmethod
    def _show_card_by_id(cls, card_id: CardId) -> None: search_executor.do_lookup(query_builder.open_card_by_id(card_id))

navigator: CardHistoryNavigator = CardHistoryNavigator()

def init() -> None:
    gui_hooks.card_will_show.append(navigator.on_card_shown)
