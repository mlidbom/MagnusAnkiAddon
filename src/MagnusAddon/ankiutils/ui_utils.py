from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from ankiutils import app
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.notes import Note
    from note.jpnote import JPNote

import aqt
from ankiutils.audio_suppressor import audio_suppressor
from ankiutils.ui_utils_interface import IUIUtils
from aqt import AnkiQt  # type: ignore
from aqt.browser import Browser  # type: ignore
from aqt.browser.previewer import Previewer
from aqt.clayout import CardLayout
from aqt.editcurrent import EditCurrent
from aqt.editor import Editor
from aqt.reviewer import RefreshNeeded
from aqt.utils import tooltip
from aqt.webview import AnkiWebView, AnkiWebViewKind
from sysutils import app_thread_pool, timeutil
from sysutils.typed import checked_cast, non_optional

_ANSWER_DISPLAY_TYPES = {'reviewAnswer', 'previewAnswer', 'clayoutAnswer'}

def main_window() -> AnkiQt: return non_optional(aqt.mw)
def is_displaytype_displaying_answer(display_type: str) -> bool:
    return display_type in _ANSWER_DISPLAY_TYPES

def is_displaytype_displaying_review_question(display_type: str) -> bool:
    return display_type == "reviewQuestion"

def is_displaytype_displaying_review_answer(display_type: str) -> bool:
    return display_type == "reviewAnswer"

def get_note_from_web_view(view: AnkiWebView) -> Optional[JPNote]:
    inner_note: Note | None

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

    from note.jpnote import JPNote
    return JPNote.note_from_note(inner_note)

class UIUtils(IUIUtils):
    def __init__(self, mw: AnkiQt) -> None:
        self._mw = mw

    def is_edit_current_open(self) -> bool:
        edit_current = [window for window in self._mw.app.topLevelWidgets() if isinstance(window, EditCurrent)]
        return len(edit_current) > 0

    def run_ui_action(self, callback: Callable[[], None]) -> None:
        time = timeutil.time_execution(callback)
        self.refresh()
        tooltip(f"done in {time}")


    def refresh(self, refresh_browser:bool = True) -> None:
        if not app.is_initialized():
            return

        def force_previewer_rerender() -> None:
            previewers: list[Previewer] = [window for window in self._mw.app.topLevelWidgets() if isinstance(window, Previewer)]
            if len(previewers) > 0:
                previewer = previewers[0]
                # noinspection PyProtectedMember
                previewer._last_state = (previewer._state, non_optional(previewer.card()).id, 0)
                previewer.render_card()

        def force_reviewer_rerender() -> None:
            if self._mw.reviewer.card:
                self._mw.reviewer._refresh_needed = RefreshNeeded.NOTE_TEXT
                self._mw.reviewer.refresh_if_needed()

        def force_browser_rerender() -> None:
            browser: list[Browser] = [window for window in self._mw.app.topLevelWidgets() if isinstance(window, Browser)]
            if len(browser) > 0:
                browser[0].onSearchActivated()

        app.col().flush_cache_updates()
        audio_suppressor.suppress_for_seconds(.3)
        force_reviewer_rerender()
        force_previewer_rerender()

        if refresh_browser:
            force_browser_rerender()

    def activate_preview(self) -> None:
        browser: Browser = aqt.dialogs.open('Browser', self._mw) # noqa
        self._mw.app.processEvents()
        if browser._previewer is None: # noqa
            browser.onTogglePreview()
        else:
            browser._previewer.activateWindow() # noqa

    def tool_tip(self, message: str, milliseconds:int = 3000) -> None:
        def show_tooltip() -> None:
            tooltip(message, milliseconds)
            QApplication.processEvents()

        app_thread_pool.run_on_ui_thread_fire_and_forget(show_tooltip)

def try_get_card_being_reviewed() -> Card | None:
    return main_window().reviewer.card