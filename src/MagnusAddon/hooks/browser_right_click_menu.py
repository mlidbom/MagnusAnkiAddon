from aqt.browser import Browser  # type: ignore
from PyQt6.QtWidgets import QMenu
from aqt import gui_hooks
from ankiutils import app
from note import queue_manager
from typing import Sequence
from anki.cards import Card
from sysutils.typed import checked_cast

def spread_due_dates(cards: Sequence[int], start_day: int, days: int) -> None:
    anki_col = app.col().anki_collection
    scheduler = anki_col.sched
    for index, card_id in enumerate(cards):
        card: Card = anki_col.get_card(card_id)
        new_due = start_day + (index * days)
        scheduler.set_due_date([card.id], str(new_due))

    app.ui_utils().refresh()

def setup_browser_context_menu(browser: Browser, menu: QMenu) -> None:
    magnus_menu: QMenu = checked_cast(QMenu, menu.addMenu("&Magnus"))
    selected_cards = browser.selected_cards()

    if len(selected_cards) == 1:
        magnus_menu.addAction("Prioritize selected cards", lambda: queue_manager.prioritize_selected_cards(selected_cards))

    if len(selected_cards) > 0:
        spread_menu: QMenu = checked_cast(QMenu, magnus_menu.addMenu("&Spread selected cards"))
        for start_day in [0,1,2,3,4,5,6,7,8,9]:
            start_day_menu: QMenu = checked_cast(QMenu, spread_menu.addMenu(f"First card in {start_day} days"))
            for days in [1,2,3,4,5,6,7,8,9]:
                start_day_menu.addAction(f"{days} days apart", lambda _start_day=start_day, _days_apart=days: spread_due_dates(selected_cards, _start_day, _days_apart))

def init() -> None:
    gui_hooks.browser_will_show_context_menu.append(setup_browser_context_menu)
