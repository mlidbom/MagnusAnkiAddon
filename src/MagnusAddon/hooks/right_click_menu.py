# coding: utf-8

from PyQt6.QtWidgets import QMenu
from anki.cards import Card
from aqt import mw, gui_hooks

from aqt.browser.previewer import Previewer
from aqt.webview import AnkiWebView, AnkiWebViewKind

from hooks.right_click_menu_note import setup_note_menu
from hooks.right_click_menu_search import setup_search_menu
from note.mynote import MyNote
from sysutils import my_clipboard


def register_lookup_actions(view: AnkiWebView, root_menu: QMenu):
    def get_card() -> MyNote:
        def get_card_inner() -> Card:
            if view.kind == AnkiWebViewKind.MAIN:
                return mw.reviewer.card
            if view.kind == AnkiWebViewKind.PREVIEWER:
                return [window for window in mw.app.topLevelWidgets() if isinstance(window, Previewer)][0].card()

        card = get_card_inner()
        if card:
            return MyNote.note_from_card(card)

    selection = view.page().selectedText().strip()
    sel_clip = selection
    if not sel_clip:
        sel_clip = my_clipboard.get_text().strip()

    note = get_card()
    if not sel_clip and not note:
        return

    setup_note_menu(note, root_menu, sel_clip, selection, view)
    setup_search_menu(root_menu, sel_clip)


def init() -> None:
    gui_hooks.webview_will_show_context_menu.append(register_lookup_actions)
    gui_hooks.editor_will_show_context_menu.append(register_lookup_actions)


