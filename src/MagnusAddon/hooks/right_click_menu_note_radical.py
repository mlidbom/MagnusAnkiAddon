from PyQt6.QtWidgets import QMenu

from ankiutils import query_builder
from hooks.right_click_menu_utils import add_lookup_action
from note.radicalnote import RadicalNote
from sysutils.typed import non_optional
from hooks import shortcutfinger

def setup_note_menu(note: RadicalNote, note_menu: QMenu, _string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu: QMenu = non_optional(note_menu.addMenu(shortcutfinger.home1("Open")))
    add_lookup_action(note_lookup_menu, shortcutfinger.home1("Kanji"), query_builder.kanji_with_radical(note))