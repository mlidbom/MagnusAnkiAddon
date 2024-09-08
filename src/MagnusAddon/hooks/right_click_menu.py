from anki.notes import Note
from aqt.clayout import CardLayout
from aqt.editor import Editor
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWidgets import QMenu
from anki.cards import Card
from aqt import gui_hooks

from aqt.browser.previewer import Previewer
from aqt.webview import AnkiWebView, AnkiWebViewKind

from ankiutils.app import main_window
from hooks.right_click_menu_note import setup_note_menu
from hooks.right_click_menu_search import setup_anki_open_menu, setup_web_search_menu
from note.jpnote import JPNote
from sysutils import my_clipboard
from sysutils.typed import checked_cast

from typing import Optional

def register_lookup_actions(view: AnkiWebView, root_menu: QMenu) -> None:
    def get_note() -> Optional[JPNote]:
        inner_note: Optional[Note]

        if view.kind == AnkiWebViewKind.MAIN:
            card = main_window().reviewer.card
            if card:
                inner_note = checked_cast(Card, main_window().reviewer.card).note()
            else:
                return None
        elif view.kind == AnkiWebViewKind.EDITOR:
            editor = checked_cast(Editor,view._bridge_context) # noqa
            card = checked_cast(Card, editor.card)
            inner_note = checked_cast(Note, card.note())
        elif view.kind == AnkiWebViewKind.PREVIEWER:
            inner_note = checked_cast(Card, [window for window in main_window().app.topLevelWidgets() if isinstance(window, Previewer)][0].card()).note()
        elif view.kind == AnkiWebViewKind.CARD_LAYOUT:
            inner_note = checked_cast(Note, [window for window in main_window().app.topLevelWidgets() if isinstance(window, CardLayout)][0].note)
        else:
            return None

        return JPNote.note_from_note(inner_note)

    selection = checked_cast(QWebEnginePage, view.page()).selectedText().strip()
    sel_clip = selection
    if not sel_clip:
        sel_clip = my_clipboard.get_text().strip()

    note = get_note()

    if sel_clip:
        setup_anki_open_menu(root_menu, sel_clip)

    if note:
        setup_note_menu(note, root_menu, sel_clip)

    if sel_clip:
        setup_web_search_menu(root_menu, sel_clip)

def init() -> None:
    gui_hooks.webview_will_show_context_menu.append(register_lookup_actions)
    gui_hooks.editor_will_show_context_menu.append(register_lookup_actions)
