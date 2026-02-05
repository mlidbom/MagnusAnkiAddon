"""
Avalonia UI integration for JAStudio.

This module provides Python wrappers for the C# Avalonia UI dialogs.
Call initialize() once at addon startup, then use the show_* functions.
"""
from __future__ import annotations

import typing

import pyperclip
from aqt import gui_hooks
from jaslib import app
from jaslib.batches import local_note_updater
from jaslib.note.kanjinote import KanjiNote
from jaslib.note.note_constants import Mine
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib.note.vocabulary.vocabnote import VocabNote
from jaspythonutils.sysutils import ex_lambda, typed
from jaspythonutils.sysutils.typed import non_optional
from typed_linq_collections.collections.q_list import QList

from jastudio.anki_extentions.note_ex import NoteEx
from jastudio.ankiutils import query_builder, search_executor, ui_utils
from jastudio.qt_utils.ex_qmenu import ExQmenu
from jastudio.ui import menus
from jastudio.ui.menus.menu_utils import shortcutfinger
from jastudio.ui.menus.menu_utils.ex_qmenu import add_ui_action, create_note_action, create_vocab_note_action
from jastudio.ui.menus.open_in_anki import build_open_in_anki_menu
from jastudio.ui.menus.web_search import build_web_search_menu

if typing.TYPE_CHECKING:
    from aqt.webview import AnkiWebView
    from jaslib.note.jpnote import JPNote
    from PyQt6.QtWidgets import QMenu

def build_browser_right_click_menu(root_menu: QMenu, note: JPNote) -> None:
    build_right_click_menu(root_menu, note, "", "")

def build_right_click_menu_webview_hook(view: AnkiWebView, root_menu: QMenu) -> None:
    selection = non_optional(view.page()).selectedText().strip()
    clipboard = pyperclip.paste().strip()
    note = ui_utils.get_note_from_web_view(view)
    build_right_click_menu(root_menu, note, selection, clipboard)

# noinspection PyPep8
def build_right_click_menu(right_click_menu: QMenu, note: JPNote | None, selection: str, clipboard: str) -> None:
    import jastudio.ankiutils.app
    if not jastudio.ankiutils.app.is_initialized():
        right_click_menu.addAction(Mine.app_still_loading_message)  # pyright: ignore[reportUnknownMemberType]
        return

    selection_menu = non_optional(right_click_menu.addMenu(shortcutfinger.home1(f'''Selection: "{selection[:40]}"'''))) if selection else None
    clipboard_menu = non_optional(right_click_menu.addMenu(shortcutfinger.home2(f'''Clipboard: "{clipboard[:40]}"'''))) if clipboard else None
    note_actions_menu = non_optional(right_click_menu.addMenu(shortcutfinger.home3("Note actions")))
    build_universal_note_actions_menu(non_optional(right_click_menu.addMenu(shortcutfinger.home4("Universal note actions"))), note)
    view_menu = non_optional(right_click_menu.addMenu(shortcutfinger.home5("View")))

    string_note_menu_factory: typing.Callable[[QMenu, str], None] = null_op_factory
    if note:
        if isinstance(note, KanjiNote):
            menus.notes.kanji.main.build_note_menu(note_actions_menu, note)
            menus.notes.kanji.main.build_view_menu(view_menu, note)
            string_note_menu_factory = lambda menu, string: menus.notes.kanji.string_menu.build(menu, typed.checked_cast(KanjiNote, note), string)  # noqa: E731
        elif isinstance(note, VocabNote):
            menus.notes.vocab.main.setup_note_menu(note_actions_menu, note, selection, clipboard)
            menus.notes.vocab.main.build_view_menu(view_menu, note)
            string_note_menu_factory = lambda menu, string: menus.notes.vocab.string_menu.build_string_menu(menu, typed.checked_cast(VocabNote, note), string)  # noqa: E731
        elif isinstance(note, SentenceNote):
            menus.notes.sentence.main.build_note_menu(note_actions_menu, note)
            menus.notes.sentence.main.build_view_menu(view_menu)
            string_note_menu_factory = lambda menu, string: menus.notes.sentence.string_menu.build_string_menu(menu, typed.checked_cast(SentenceNote, note), string)  # noqa: E731

    if selection_menu:
        build_string_menu(selection_menu, selection, string_note_menu_factory)
    if clipboard_menu:
        build_string_menu(clipboard_menu, clipboard, string_note_menu_factory)

    # Add Avalonia menu entry (proof of concept)
    _add_avalonia_menu_entry(right_click_menu, selection, clipboard)

    ExQmenu.disable_empty_submenus(right_click_menu)

def build_string_menu(menu: QMenu, string: str, string_note_menu_factory: typing.Callable[[QMenu, str], None]) -> None:
    def build_create_note_menu(create_note_menu: QMenu, to_create: str) -> None:
        create_vocab_note_action(create_note_menu, shortcutfinger.home1("vocab"), ex_lambda.bind1(VocabNote.factory.create_with_dictionary, string))
        create_note_action(create_note_menu, shortcutfinger.home2("sentence"), ex_lambda.bind1(SentenceNote.create, to_create))
        create_note_action(create_note_menu, shortcutfinger.home3("kanji"), ex_lambda.bind4(KanjiNote.create, to_create, "TODO", "", ""))

    def build_matching_note_menu(matching_note_menu: QMenu, search_string: str) -> None:
        vocabs = list(app.col().vocab.with_question_prefer_disambiguation_name(search_string))
        sentences = app.col().sentences.with_question(search_string)
        kanjis = app.col().kanji.with_any_kanji_in([search_string]) if len(search_string) == 1 else QList[KanjiNote]()

        if not any(vocabs) and not any(sentences) and not any(kanjis):
            return

        build_universal_note_actions_menu(non_optional(matching_note_menu.addMenu(shortcutfinger.home1("Vocab Actions"))), vocabs[0] if vocabs else None)
        build_universal_note_actions_menu(non_optional(matching_note_menu.addMenu(shortcutfinger.home2("Sentence Actions"))), sentences[0] if sentences else None)
        build_universal_note_actions_menu(non_optional(matching_note_menu.addMenu(shortcutfinger.home3("Kanji Actions"))), kanjis[0] if kanjis else None)

    string_note_menu_factory(non_optional(menu.addMenu(shortcutfinger.home1("Current note actions"))), string)
    build_open_in_anki_menu(non_optional(menu.addMenu(shortcutfinger.home2("Open in Anki"))), lambda: string)
    build_web_search_menu(non_optional(menu.addMenu(shortcutfinger.home3("Search Web"))), lambda: string)
    build_matching_note_menu(non_optional(menu.addMenu(shortcutfinger.home4("Exactly matching notes"))), string)
    build_create_note_menu(non_optional(menu.addMenu(shortcutfinger.up1(f"Create: {string[:40]}"))), string)
    add_ui_action(menu, shortcutfinger.down1("Reparse matching sentences"), lambda: local_note_updater.reparse_matching_sentences(string))

def build_universal_note_actions_menu(universal_actions_menu: QMenu, note: JPNote | None) -> None:
    if not note: return

    note_ex = NoteEx.from_note(note)

    universal_actions_menu.addAction(shortcutfinger.home1("Open in previewer"), search_executor.lookup_and_show_previewer_promise(lambda: query_builder.notes_lookup([note])))  # pyright: ignore[reportUnknownMemberType]
    note_actions_menu = non_optional(universal_actions_menu.addMenu(shortcutfinger.home2("Note actions")))

    add_ui_action(universal_actions_menu, shortcutfinger.home3("Unsuspend all cards"), note_ex.un_suspend_all_cards, note_ex.has_suspended_cards())
    add_ui_action(universal_actions_menu, shortcutfinger.home4("Suspend all cards"), note_ex.suspend_all_cards, note_ex.has_active_cards())
    # add_ui_action(universal_actions_menu, shortcutfinger.up1("Unsuspend all cards and dependencies' cards"), note.unsuspend_all_cards_and_dependencies, confirm=True, enabled=note.has_suspended_cards_or_depencies_suspended_cards())

    if note:
        if isinstance(note, KanjiNote):
            menus.notes.kanji.main.build_note_menu(note_actions_menu, note)
        elif isinstance(note, VocabNote):
            menus.notes.vocab.main.setup_note_menu(note_actions_menu, note, "TODO:selection", "TODO:clipboard")
        elif isinstance(note, SentenceNote):
            menus.notes.sentence.main.build_note_menu(note_actions_menu, note)

def null_op_factory(_menu: QMenu, _string: str) -> None:
    pass


def _add_avalonia_menu_entry(menu: QMenu, selection: str, clipboard: str) -> None:
    """Add Avalonia menu entry that shows Avalonia popup on hover."""
    from jastudio.ui import avalonia_host
    from jastudio.ui.avalonia_menu_helper import add_hover_avalonia_menu
    from jastudio.ui.tools_menu import refresh

    def show_context_menu(physical_x: int, physical_y: int) -> None:
        """Show the appropriate context menu based on current note type."""
        # Determine note type and show appropriate menu
        note = ui_utils.try_get_review_note()
        if note:
            from jaslib.note.kanjinote import KanjiNote
            from jaslib.note.sentences.sentencenote import SentenceNote
            from jaslib.note.vocabulary.vocabnote import VocabNote

            if isinstance(note, VocabNote):
                avalonia_host.show_vocab_context_menu(refresh, selection, clipboard, physical_x, physical_y)
            elif isinstance(note, KanjiNote):
                avalonia_host.show_kanji_context_menu(refresh, selection, clipboard, physical_x, physical_y)
            elif isinstance(note, SentenceNote):
                avalonia_host.show_sentence_context_menu(refresh, selection, clipboard, physical_x, physical_y)
            else:
                avalonia_host.show_generic_context_menu(refresh, selection, clipboard, physical_x, physical_y)
        else:
            avalonia_host.show_generic_context_menu(refresh, selection, clipboard, physical_x, physical_y)

    add_hover_avalonia_menu(menu, shortcutfinger.up1("🎯 AvaloniaMenu (Hover to show)"), show_context_menu)


def init() -> None:
    gui_hooks.webview_will_show_context_menu.append(build_right_click_menu_webview_hook)  # pyright: ignore[reportUnknownMemberType]
    gui_hooks.editor_will_show_context_menu.append(build_right_click_menu_webview_hook)  # pyright: ignore[reportUnknownMemberType]
