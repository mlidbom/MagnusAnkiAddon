import pyperclip  # type: ignore
from anki.notes import Note
from aqt.clayout import CardLayout
from aqt.editor import Editor
from PyQt6.QtWidgets import QMenu
from aqt import gui_hooks

from aqt.browser.previewer import Previewer
from aqt.webview import AnkiWebView, AnkiWebViewKind

from ankiutils import query_builder, search_executor
from ankiutils.app import main_window
from batches import local_note_updater
from hooks import right_click_menu_note_radical, right_click_menu_note_kanji, right_click_menu_note_vocab, right_click_menu_note_sentence
from hooks.right_click_menu_search import setup_anki_open_menu, setup_web_search_menu
from hooks.right_click_menu_utils import add_ui_action, create_note_action, create_vocab_note_action
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.radicalnote import RadicalNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils.typed import checked_cast, non_optional

from typing import Optional
from hooks import shortcutfinger

def register_lookup_actions(view: AnkiWebView, root_menu: QMenu) -> None:
    def get_note() -> Optional[JPNote]:
        inner_note: Optional[Note]

        if view.kind == AnkiWebViewKind.MAIN:
            card = main_window().reviewer.card
            if card:
                inner_note = non_optional(main_window().reviewer.card).note()
            else:
                return None
        elif view.kind == AnkiWebViewKind.EDITOR:
            # noinspection PyProtectedMember
            editor = checked_cast(Editor, view._bridge_context)
            if not editor.card: return None
            card = non_optional(editor.card)
            inner_note = non_optional(card.note())
        elif view.kind == AnkiWebViewKind.PREVIEWER:
            inner_note = non_optional([window for window in main_window().app.topLevelWidgets() if isinstance(window, Previewer)][0].card()).note()
        elif view.kind == AnkiWebViewKind.CARD_LAYOUT:
            inner_note = non_optional([window for window in main_window().app.topLevelWidgets() if isinstance(window, CardLayout)][0].note)
        else:
            return None

        return JPNote.note_from_note(inner_note)

    selection = non_optional(view.page()).selectedText().strip()
    clipboard = pyperclip.paste().strip()

    note = get_note()

    string_menus: list[tuple[QMenu, str]] = []
    if selection:
        string_menus.append((non_optional(root_menu.addMenu(shortcutfinger.home1(f'''Selection: "{selection[:40]}"'''))), selection))
    if clipboard:
        string_menus.append((non_optional(root_menu.addMenu(shortcutfinger.home2(f'''Clipboard: "{clipboard[:40]}"'''))), clipboard))

    if note:
        setup_note_menu(note, root_menu, string_menus, selection, clipboard)

    for string_menu, menu_string in string_menus:
        string_menu.addSeparator()

    for string_menu, menu_string in string_menus:
        setup_matching_note_menu(string_menu, menu_string)

    for string_menu, menu_string in string_menus:
        setup_anki_open_menu(string_menu, menu_string)

    for string_menu, menu_string in string_menus:
        setup_web_search_menu(string_menu, menu_string)

    for string_menu, menu_string in string_menus:
        add_ui_action(string_menu, "remove from sentence exclusions", lambda _string=menu_string: local_note_updater.clean_sentence_excluded_word(_string))# type: ignore

    for string_menu, menu_string in string_menus:
        create_menu = non_optional(string_menu.addMenu(shortcutfinger.down2(f"Create: {menu_string}")))
        create_vocab_note_action(create_menu, shortcutfinger.home1(f"vocab"), lambda _string=menu_string: VocabNote.create_with_dictionary(_string)) # type: ignore
        create_note_action(create_menu, shortcutfinger.home2(f"sentence"), lambda _word=menu_string: SentenceNote.create(_word)) # type: ignore
        create_note_action(create_menu, shortcutfinger.home3(f"kanji"), lambda _word=menu_string: KanjiNote.create(_word, "TODO", "", "")) # type: ignore


def create_note_actions_menu(note_menu: QMenu, note:JPNote, title:str) -> None:
    menu = non_optional(note_menu.addMenu(title))

    menu.addAction(shortcutfinger.home1("Open"), search_executor.lookup_promise(lambda: query_builder.notes_lookup([note])))
    menu.addAction(shortcutfinger.home2("Open in previewer"), search_executor.lookup_and_show_previewer_promise(lambda: query_builder.notes_lookup([note])))

    if note.has_suspended_cards():
        add_ui_action(menu, shortcutfinger.home3("Unsuspend all cards"), note.unsuspend_all_cards)
    elif note.has_active_cards():
        add_ui_action(menu, shortcutfinger.home3("Suspend all cards"), note.suspend_all_cards)

    if note.has_suspended_cards_or_depencies_suspended_cards():
        add_ui_action(menu, shortcutfinger.home4("Unsuspend all cards and dependencies' cards"), note.unsuspend_all_cards_and_dependencies, confirm=True)

def setup_note_menu(note: JPNote, root_menu: QMenu, string_menus: list[tuple[QMenu, str]], selection:str = "", clipboard:str = "") -> None:
    note_menu = non_optional(root_menu.addMenu(shortcutfinger.home3("Note")))
    if isinstance(note, RadicalNote):
        right_click_menu_note_radical.setup_note_menu(note, note_menu, string_menus)
    elif isinstance(note, KanjiNote):
        right_click_menu_note_kanji.setup_note_menu(note, note_menu, string_menus)
    elif isinstance(note, VocabNote):
        right_click_menu_note_vocab.setup_note_menu(note, note_menu, string_menus, selection, clipboard)
    elif isinstance(note, SentenceNote):
        right_click_menu_note_sentence.setup_note_menu(note, note_menu, string_menus)

    create_note_actions_menu(note_menu, note, shortcutfinger.home4("Note actions"))

def setup_matching_note_menu(string_menu: QMenu, string:str) -> None:
    from ankiutils import app
    vocabs = app.col().vocab.with_question(string)
    sentences = app.col().sentences.with_question(string)
    kanjis = app.col().kanji.with_any_kanji_in([string]) if len(string) == 1 else []

    if any(vocabs) or any(sentences) or any(kanjis):
        note_menu = non_optional(string_menu.addMenu(shortcutfinger.home4("Notes")))
        if any(vocabs):
            create_note_actions_menu(note_menu, vocabs[0], shortcutfinger.home1("Vocab Actions"))
        if any(sentences):
            create_note_actions_menu(note_menu, sentences[0], shortcutfinger.home2("Sentence Actions"))
        if any(kanjis):
            create_note_actions_menu(note_menu, kanjis[0], shortcutfinger.home3("Kanji Actions"))

def init() -> None:
    gui_hooks.webview_will_show_context_menu.append(register_lookup_actions)
    gui_hooks.editor_will_show_context_menu.append(register_lookup_actions)
