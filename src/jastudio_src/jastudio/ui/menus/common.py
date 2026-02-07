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

    _add_csharp_menu_entry(right_click_menu, note, selection, clipboard)

    ExQmenu.disable_empty_submenus(right_click_menu)



def _add_csharp_menu_entry(right_click_menu: QMenu, note: JPNote | None, selection: str, clipboard: str) -> None:
    from jas_dotnet.qt_adapters import qt_menu_adapter

    from jastudio.ui import app_root
    menu_builder = app_root.CreateNoteContextMenu()

    try:
        if note:
            if isinstance(note, VocabNote):
                specs = menu_builder.BuildVocabContextMenuSpec(note.get_id(), selection, clipboard)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            elif isinstance(note, KanjiNote):
                specs = menu_builder.BuildKanjiContextMenuSpec(note.get_id(), selection, clipboard)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            elif isinstance(note, SentenceNote):
                specs = menu_builder.BuildSentenceContextMenuSpec(note.get_id(), selection, clipboard)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            else:
                specs = menu_builder.BuildGenericContextMenuSpec(selection, clipboard)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        else:
            specs = menu_builder.BuildGenericContextMenuSpec(selection, clipboard)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]


        qt_menu_adapter.add_to_qt_menu(right_click_menu, specs)  # pyright: ignore[reportUnknownArgumentType]
    except Exception as e:
        from jaslib import mylog
        mylog.error(f"Failed to build C# menus: {e}")
        import traceback
        mylog.error(traceback.format_exc())
        # Add fallback menu item
        right_click_menu.addAction("⚠️ C# Menu Error (check console)")  # pyright: ignore[reportUnknownMemberType]


def init() -> None:
    gui_hooks.webview_will_show_context_menu.append(build_right_click_menu_webview_hook)  # pyright: ignore[reportUnknownMemberType]
    gui_hooks.editor_will_show_context_menu.append(build_right_click_menu_webview_hook)  # pyright: ignore[reportUnknownMemberType]
