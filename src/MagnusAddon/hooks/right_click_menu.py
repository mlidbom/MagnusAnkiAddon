from PyQt6.QtWidgets import QMenu
from anki.cards import Card
from aqt import gui_hooks

from aqt.browser.previewer import Previewer
from aqt.webview import AnkiWebView, AnkiWebViewKind

from ankiutils.app import main_window
from hooks.right_click_menu_note import setup_note_menu
from hooks.right_click_menu_search import setup_search_menu
from note.jpnote import JPNote
from sysutils import my_clipboard
from sysutils.typed import checked_cast


def register_lookup_actions(view: AnkiWebView, root_menu: QMenu) -> None:
    def get_note() -> JPNote:
        def get_card_inner() -> Card:
            if view.kind == AnkiWebViewKind.MAIN:
                return checked_cast(Card, main_window().reviewer.card)
            if view.kind == AnkiWebViewKind.PREVIEWER:
                return checked_cast(Card, [window for window in main_window().app.topLevelWidgets() if isinstance(window, Previewer)][0].card())

            raise Exception("Failed to find card")

        return JPNote.note_from_card(get_card_inner())


    selection = view.page().selectedText().strip()
    sel_clip = selection
    if not sel_clip:
        sel_clip = my_clipboard.get_text().strip()

    note = get_note()
    if not sel_clip and not note:
        return

    setup_note_menu(note, root_menu, sel_clip, selection, view)
    setup_search_menu(root_menu, sel_clip)


def init() -> None:
    gui_hooks.webview_will_show_context_menu.append(register_lookup_actions)
    gui_hooks.editor_will_show_context_menu.append(register_lookup_actions)


