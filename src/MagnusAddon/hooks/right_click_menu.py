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
from hooks import right_click_menu_note_radical, right_click_menu_note_kanji, right_click_menu_note_vocab, right_click_menu_note_sentence
from hooks.right_click_menu_search import setup_anki_open_menu, setup_web_search_menu
from hooks.right_click_menu_utils import add_ui_action
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.radicalnote import RadicalNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import my_clipboard
from sysutils.typed import checked_cast

from typing import Optional
from hooks import shortcutfinger
from ankiutils import query_builder, search_executor

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
    clipboard = my_clipboard.get_text().strip()

    note = get_note()

    string_menus: list[tuple[QMenu, str]] = []
    if selection:
        string_menus.append((checked_cast(QMenu, root_menu.addMenu(shortcutfinger.home1(f'''Selection: "{selection[:40]}"'''))), selection))
    if clipboard:
        string_menus.append((checked_cast(QMenu, root_menu.addMenu(shortcutfinger.home2(f'''Clipboard: "{clipboard[:40]}"'''))), clipboard))

    if note:
        setup_note_menu(note, root_menu, string_menus)

    for string_menu, menu_string in string_menus:
        string_menu.addSeparator()

    for string_menu, menu_string in string_menus:
        setup_anki_open_menu(string_menu, menu_string)

    for string_menu, menu_string in string_menus:
        setup_web_search_menu(string_menu, menu_string)

    for string_menu, menu_string in string_menus:
        setup_matching_note_menu(string_menu, menu_string)

def setup_note_menu(note: JPNote, root_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_menu = checked_cast(QMenu, root_menu.addMenu(shortcutfinger.home3("Note")))
    if isinstance(note, RadicalNote):
        right_click_menu_note_radical.setup_note_menu(note, note_menu, string_menus)
    if isinstance(note, KanjiNote):
        right_click_menu_note_kanji.setup_note_menu(note, note_menu, string_menus)
    if isinstance(note, VocabNote):
        right_click_menu_note_vocab.setup_note_menu(note, note_menu, string_menus)
    if isinstance(note, SentenceNote):
        right_click_menu_note_sentence.setup_note_menu(note, note_menu, string_menus)


def setup_matching_note_menu(string_menu: QMenu, string:str) -> None:
    from ankiutils import app
    vocabs = app.col().vocab.with_question(string)
    sentences = app.col().sentences.with_question(string)

    kanjis = app.col().kanji.with_any_kanji_in([string]) if len(string) == 1 else []

    def add_note_actions(note:JPNote, menu: QMenu) -> None:
        menu.addAction(shortcutfinger.home1("Open"), search_executor.lookup_promise(lambda: query_builder.notes_lookup([note])))
        menu.addAction(shortcutfinger.home2("Open in previewer"), search_executor.lookup_and_show_previewer_promise(lambda: query_builder.notes_lookup([note])))

        if note.has_suspended_cards():
            add_ui_action(menu, shortcutfinger.home3("Unsuspend all cards"), note.unsuspend_all_cards)

        if note.has_active_cards():
            add_ui_action(menu, shortcutfinger.home4("Suspend all cards"), note.suspend_all_cards)

    if vocabs or sentences or kanjis:
        note_menu = checked_cast(QMenu, string_menu.addMenu(shortcutfinger.up1("Notes")))
        if any(vocabs):
            vocab = vocabs[0]
            add_note_actions(vocab, checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home1("Vocab"))))

        if any(sentences):
            sentence = sentences[0]
            add_note_actions(sentence, checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home2("Sentence"))))

        if any(kanjis):
            kanji = kanjis[0]
            add_note_actions(kanji, checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home3("Kanji"))))

def init() -> None:
    gui_hooks.webview_will_show_context_menu.append(register_lookup_actions)
    gui_hooks.editor_will_show_context_menu.append(register_lookup_actions)
