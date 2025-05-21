from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import query_builder
from sysutils.typed import non_optional
from ui.qt_menu import shortcutfinger
from ui.qt_menu.right_click_menu_utils import add_lookup_action

if TYPE_CHECKING:
    from note.radicalnote import RadicalNote
    from PyQt6.QtWidgets import QMenu


def setup_note_menu(note_menu: QMenu, note: RadicalNote) -> None:
    note_lookup_menu: QMenu = non_optional(note_menu.addMenu(shortcutfinger.home1("Open")))
    add_lookup_action(note_lookup_menu, shortcutfinger.home1("Kanji"), query_builder.kanji_with_radical(note))