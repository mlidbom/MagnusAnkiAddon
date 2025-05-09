from typing import Callable, Optional

import pyperclip  # type: ignore
from PyQt6.QtWidgets import QMenu
from aqt import gui_hooks

from aqt.webview import AnkiWebView

from ankiutils import query_builder, search_executor, ui_utils
from batches import local_note_updater
from hooks import right_click_menu_note_radical, right_click_menu_note_kanji, right_click_menu_note_vocab, right_click_menu_note_sentence
from hooks.right_click_menu_search import build_open_in_anki_menu, build_web_search_menu
from hooks.right_click_menu_utils import add_ui_action, create_note_action, create_vocab_note_action
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.radicalnote import RadicalNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import typed
from sysutils.typed import non_optional

from hooks import shortcutfinger

def build_browser_right_click_menu(root_menu: QMenu, note: JPNote) -> None:
    build_right_click_menu(root_menu, note, "", "")

def build_right_click_menu_webview_hook(view: AnkiWebView, root_menu: QMenu) -> None:
    selection = non_optional(view.page()).selectedText().strip()
    clipboard = pyperclip.paste().strip()
    note = ui_utils.get_note_from_web_view(view)
    build_right_click_menu(root_menu, note, selection, clipboard)

def build_right_click_menu(root_menu: QMenu, note: Optional[JPNote], selection: str, clipboard: str) -> None:
    selection_menu = non_optional(root_menu.addMenu(shortcutfinger.home1(f'''Selection: "{selection[:40]}"'''))) if selection else None
    clipboard_menu = non_optional(root_menu.addMenu(shortcutfinger.home2(f'''Clipboard: "{clipboard[:40]}"'''))) if clipboard else None

    string_note_menu_factory: Callable[[QMenu, str], None] = null_op_factory

    if note:
        if isinstance(note, RadicalNote):
            right_click_menu_note_radical.setup_note_menu(non_optional(root_menu.addMenu(shortcutfinger.home3("Radical note actions"))), note)
        elif isinstance(note, KanjiNote):
            right_click_menu_note_kanji.build_note_menu(non_optional(root_menu.addMenu(shortcutfinger.home3("Kanji note actions"))), note)
            string_note_menu_factory = lambda menu, string: right_click_menu_note_kanji.build_string_menu(menu, typed.checked_cast(KanjiNote, note), string)
        elif isinstance(note, VocabNote):
            right_click_menu_note_vocab.setup_note_menu(non_optional(root_menu.addMenu(shortcutfinger.home3("Vocab note actions"))), note, selection, clipboard)
            string_note_menu_factory = lambda menu, string: right_click_menu_note_vocab.build_string_menu(menu, typed.checked_cast(VocabNote, note), string)
        elif isinstance(note, SentenceNote):
            right_click_menu_note_sentence.build_note_menu(non_optional(root_menu.addMenu(shortcutfinger.home3("Sentence note actions"))), note)
            string_note_menu_factory = lambda menu, string: right_click_menu_note_sentence.build_string_menu(menu, typed.checked_cast(SentenceNote, note), string)

        build_universal_note_actions_menu(non_optional(root_menu.addMenu(shortcutfinger.home4("Universal note actions"))), note)

    if selection_menu:
        build_string_menu(selection_menu, selection, string_note_menu_factory)
    if clipboard_menu:
        build_string_menu(clipboard_menu, clipboard, string_note_menu_factory)

def build_string_menu(menu: QMenu, string: str, string_note_menu_factory: Callable[[QMenu, str], None]) -> None:
    def build_create_note_menu(create_note_menu: QMenu, to_create: str) -> None:
        create_vocab_note_action(create_note_menu, shortcutfinger.home1(f"vocab"), lambda _string=to_create: VocabNote.create_with_dictionary(_string))  # type: ignore
        create_note_action(create_note_menu, shortcutfinger.home2(f"sentence"), lambda _word=to_create: SentenceNote.create(_word))  # type: ignore
        create_note_action(create_note_menu, shortcutfinger.home3(f"kanji"), lambda _word=to_create: KanjiNote.create(_word, "TODO", "", ""))  # type: ignore

    def build_matching_note_menu(menu_title: str, string_menu: QMenu, search_string: str) -> None:
        from ankiutils import app
        vocabs = app.col().vocab.with_question(search_string)
        sentences = app.col().sentences.with_question(search_string)
        kanjis = app.col().kanji.with_any_kanji_in([search_string]) if len(search_string) == 1 else []

        if any(vocabs) or any(sentences) or any(kanjis):
            note_menu = non_optional(string_menu.addMenu(menu_title))
            if any(vocabs):
                build_universal_note_actions_menu(non_optional(note_menu.addMenu(shortcutfinger.home1("Vocab Actions"))), vocabs[0])
            if any(sentences):
                build_universal_note_actions_menu(non_optional(note_menu.addMenu(shortcutfinger.home2("Sentence Actions"))), sentences[0])
            if any(kanjis):
                build_universal_note_actions_menu(non_optional(note_menu.addMenu(shortcutfinger.home3("Kanji Actions"))), kanjis[0])

    string_note_menu_factory(non_optional(menu.addMenu(shortcutfinger.home2("Note actions"))), string)
    build_matching_note_menu(shortcutfinger.home2("Exactly matching notes"), menu, string)
    build_open_in_anki_menu(non_optional(menu.addMenu(shortcutfinger.home3("Open in Anki"))), lambda menu_string_=string: menu_string_)  # type: ignore
    build_web_search_menu(non_optional(menu.addMenu(shortcutfinger.home4("Search Web"))), lambda menu_string_=string: menu_string_)  # type: ignore
    build_create_note_menu(non_optional(menu.addMenu(shortcutfinger.up1(f"Create: {string}"))), string)
    add_ui_action(menu, shortcutfinger.down1("remove from sentence exclusions"), lambda _string=string: local_note_updater.clean_sentence_excluded_word(_string))  # type: ignore

def build_universal_note_actions_menu(note_actions_menu: QMenu, note: JPNote) -> None:
    note_actions_menu.addAction(shortcutfinger.home1("Find in browser"), search_executor.lookup_promise(lambda: query_builder.notes_lookup([note])))
    note_actions_menu.addAction(shortcutfinger.home2("Open in previewer"), search_executor.lookup_and_show_previewer_promise(lambda: query_builder.notes_lookup([note])))

    if note.has_suspended_cards():
        add_ui_action(note_actions_menu, shortcutfinger.home3("Unsuspend all cards"), note.unsuspend_all_cards)
    if note.has_active_cards():
        add_ui_action(note_actions_menu, shortcutfinger.home4("Suspend all cards"), note.suspend_all_cards)

    if note.has_suspended_cards_or_depencies_suspended_cards():
        add_ui_action(note_actions_menu, shortcutfinger.up1("Unsuspend all cards and dependencies' cards"), note.unsuspend_all_cards_and_dependencies, confirm=True)

def null_op_factory(_menu: QMenu, _string: str) -> None:
    pass

def init() -> None:
    gui_hooks.webview_will_show_context_menu.append(build_right_click_menu_webview_hook)
    gui_hooks.editor_will_show_context_menu.append(build_right_click_menu_webview_hook)
