from aqt.browser import Browser  # type: ignore
from PyQt6.QtWidgets import QMenu
from aqt import gui_hooks

from note import queue_manager


def setup_browser_context_menu(browser: Browser, menu: QMenu) -> None:
    selected_cards = browser.selected_cards()

    if len(selected_cards) == 1:
        menu.addAction("Prioritize selected cards", lambda: queue_manager.prioritize_selected_cards(selected_cards))

def init() -> None:
    gui_hooks.browser_will_show_context_menu.append(setup_browser_context_menu)
