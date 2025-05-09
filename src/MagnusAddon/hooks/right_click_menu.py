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

def build_right_click_menu(view: AnkiWebView, root_menu: QMenu) -> None:
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

    def build_create_menu(create_menu: QMenu, to_create: str) -> None:
        create_vocab_note_action(create_menu, shortcutfinger.home1(f"vocab"), lambda _string=to_create: VocabNote.create_with_dictionary(_string))  # type: ignore
        create_note_action(create_menu, shortcutfinger.home2(f"sentence"), lambda _word=to_create: SentenceNote.create(_word))  # type: ignore
        create_note_action(create_menu, shortcutfinger.home3(f"kanji"), lambda _word=to_create: KanjiNote.create(_word, "TODO", "", ""))  # type: ignore

    def build_string_menu(menu: QMenu, string: str) -> None:
        menu.addSeparator()
        # todo: several fingers blocked by actions that may be added by the code below that passes this menu to the setup_note_menu function.
        # We probably want to change this somehow to remove the risk of collisions
        build_matching_note_menu(shortcutfinger.home4("Notes"), menu, string)
        setup_anki_open_menu(non_optional(menu.addMenu(shortcutfinger.up1("Open in Anki"))), lambda menu_string_=string: menu_string_)  # type: ignore
        setup_web_search_menu(non_optional(menu.addMenu(shortcutfinger.down1("Search Web"))), lambda menu_string_=string: menu_string_)  # type: ignore
        build_create_menu(non_optional(menu.addMenu(shortcutfinger.down2(f"Create: {string}"))), string)
        add_ui_action(menu, "remove from sentence exclusions", lambda _string=string: local_note_updater.clean_sentence_excluded_word(_string))  # type: ignore

    selection = non_optional(view.page()).selectedText().strip()
    clipboard = pyperclip.paste().strip()

    note = get_note()

    string_menus: list[tuple[QMenu, str]] = []
    if selection:
        string_menus.append((non_optional(root_menu.addMenu(shortcutfinger.home1(f'''Selection: "{selection[:40]}"'''))), selection))
    if clipboard:
        string_menus.append((non_optional(root_menu.addMenu(shortcutfinger.home2(f'''Clipboard: "{clipboard[:40]}"'''))), clipboard))

    if note:
        build_note_menu(non_optional(root_menu.addMenu(shortcutfinger.home3("Note"))), note, string_menus, selection, clipboard)

    for string_menu, menu_string in string_menus:
        build_string_menu(string_menu, menu_string)

def build_note_menu(note_menu: QMenu, note: JPNote, string_menus: list[tuple[QMenu, str]], selection: str = "", clipboard: str = "") -> None:
    if isinstance(note, RadicalNote):
        right_click_menu_note_radical.setup_note_menu(note, note_menu, string_menus)
    elif isinstance(note, KanjiNote):
        right_click_menu_note_kanji.build_note_menu(note, note_menu)
        for string_menu, menu_string in string_menus:
            right_click_menu_note_kanji.build_string_menu(string_menu, note, menu_string)

    elif isinstance(note, VocabNote):
        right_click_menu_note_vocab.setup_note_menu(note, note_menu, string_menus, selection, clipboard)
    elif isinstance(note, SentenceNote):
        right_click_menu_note_sentence.setup_note_menu(note, note_menu, string_menus)

    build_note_actions_menu(non_optional(note_menu.addMenu(shortcutfinger.home4("Note actions"))), note)

def build_matching_note_menu(menu_title: str, string_menu: QMenu, search_string: str) -> None:
    from ankiutils import app
    vocabs = app.col().vocab.with_question(search_string)
    sentences = app.col().sentences.with_question(search_string)
    kanjis = app.col().kanji.with_any_kanji_in([search_string]) if len(search_string) == 1 else []

    if any(vocabs) or any(sentences) or any(kanjis):
        note_menu = non_optional(string_menu.addMenu(menu_title))
        if any(vocabs):
            build_note_actions_menu(non_optional(note_menu.addMenu(shortcutfinger.home1("Vocab Actions"))), vocabs[0])
        if any(sentences):
            build_note_actions_menu(non_optional(note_menu.addMenu(shortcutfinger.home2("Sentence Actions"))), sentences[0])
        if any(kanjis):
            build_note_actions_menu(non_optional(note_menu.addMenu(shortcutfinger.home3("Kanji Actions"))), kanjis[0])

def build_note_actions_menu(note_actions_menu: QMenu, note: JPNote) -> None:
    note_actions_menu.addAction(shortcutfinger.home1("Open"), search_executor.lookup_promise(lambda: query_builder.notes_lookup([note])))
    note_actions_menu.addAction(shortcutfinger.home2("Open in previewer"), search_executor.lookup_and_show_previewer_promise(lambda: query_builder.notes_lookup([note])))

    if note.has_suspended_cards():
        add_ui_action(note_actions_menu, shortcutfinger.home3("Unsuspend all cards"), note.unsuspend_all_cards)
    elif note.has_active_cards():
        add_ui_action(note_actions_menu, shortcutfinger.home3("Suspend all cards"), note.suspend_all_cards)

    if note.has_suspended_cards_or_depencies_suspended_cards():
        add_ui_action(note_actions_menu, shortcutfinger.home4("Unsuspend all cards and dependencies' cards"), note.unsuspend_all_cards_and_dependencies, confirm=True)

def init() -> None:
    gui_hooks.webview_will_show_context_menu.append(build_right_click_menu)
    gui_hooks.editor_will_show_context_menu.append(build_right_click_menu)
