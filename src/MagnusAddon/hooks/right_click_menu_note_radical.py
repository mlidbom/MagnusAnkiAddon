from PyQt6.QtWidgets import QMenu

from ankiutils import query_builder
from hooks.right_click_menu_utils import add_lookup_action
from note.radicalnote import RadicalNote
from sysutils.typed import checked_cast

def setup_note_menu(note: RadicalNote, note_menu: QMenu, _string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu: QMenu = checked_cast(QMenu, note_menu.addMenu("&Open"))
    add_lookup_action(note_lookup_menu, "&Kanji", query_builder.kanji_with_radical(note))