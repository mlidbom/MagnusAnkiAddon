from __future__ import annotations

import typing

import pyperclip
from aqt import gui_hooks
from jaslib.note.kanjinote import KanjiNote
from jaslib.note.note_constants import Mine
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib.note.vocabulary.vocabnote import VocabNote
from jaspythonutils.sysutils.typed import non_optional

from jastudio.ankiutils import ui_utils
from jastudio.qt_utils.ex_qmenu import ExQmenu

if typing.TYPE_CHECKING:
    from aqt.webview import AnkiWebView
    from JAStudio.Core.Note import JPNote
    from PyQt6.QtWidgets import QMenu

def build_browser_right_click_menu(root_menu: QMenu, note: JPNote) -> None:
    build_right_click_menu(root_menu, note, "", "")

def build_right_click_menu_webview_hook(view: AnkiWebView, root_menu: QMenu) -> None:
    selection = non_optional(view.page()).selectedText().strip()
    clipboard = pyperclip.paste().strip()
    note = ui_utils.get_note_from_web_view(view)
    build_right_click_menu(root_menu, note, selection, clipboard)

def build_right_click_menu(right_click_menu: QMenu, note: JPNote | None, selection: str, clipboard: str) -> None:
    import jastudio.ankiutils.app
    if not jastudio.ankiutils.app.is_initialized():
        right_click_menu.addAction(Mine.app_still_loading_message)  # pyright: ignore[reportUnknownMemberType]
        return

    from jas_dotnet.qt_adapters import qt_menu_adapter

    from jastudio.ui import dotnet_ui_root
    menu_builder = dotnet_ui_root.CreateNoteContextMenu()

    try:
        if note:
            if isinstance(note, VocabNote):
                specs = menu_builder.BuildVocabContextMenuSpec(note.get_id(), selection, clipboard)
            elif isinstance(note, KanjiNote):
                specs = menu_builder.BuildKanjiContextMenuSpec(note.get_id(), selection, clipboard)
            elif isinstance(note, SentenceNote):
                specs = menu_builder.BuildSentenceContextMenuSpec(note.get_id(), selection, clipboard)
            else:
                specs = menu_builder.BuildGenericContextMenuSpec(selection, clipboard)
        else:
            specs = menu_builder.BuildGenericContextMenuSpec(selection, clipboard)


        qt_menu_adapter.add_to_qt_menu(right_click_menu, specs)
    except Exception as e:
        from jaslib import mylog
        mylog.error(f"Failed to build C# menus: {e}")
        import traceback
        mylog.error(traceback.format_exc())
        # Add fallback menu item
        right_click_menu.addAction("⚠️ C# Menu Error (check console)")  # pyright: ignore[reportUnknownMemberType]

    ExQmenu.disable_empty_submenus(right_click_menu)


def init() -> None:
    gui_hooks.webview_will_show_context_menu.append(build_right_click_menu_webview_hook)  # pyright: ignore[reportUnknownMemberType]
    gui_hooks.editor_will_show_context_menu.append(build_right_click_menu_webview_hook)  # pyright: ignore[reportUnknownMemberType]
