from typing import Any, Callable

import aqt
from aqt import AnkiQt  # type: ignore
from aqt.browser import Browser  # type: ignore
from aqt.browser.previewer import Previewer
from aqt.editcurrent import EditCurrent
from aqt.reviewer import RefreshNeeded
from aqt.utils import tooltip
from PyQt6.QtGui import QAction

from ankiutils.audio_suppressor import audio_suppressor
from ankiutils.ui_utils_interface import IUIUtils
from sysutils import timeutil
from sysutils.typed import non_optional
from typing import Optional
from PyQt6.QtWidgets import QPushButton, QWidget

_ANSWER_DISPLAY_TYPES = {'reviewAnswer', 'previewAnswer', 'clayoutAnswer'}

def is_displaytype_displaying_answer(display_type: str) -> bool:
    return display_type in _ANSWER_DISPLAY_TYPES

def is_displaytype_displaying_review_question(display_type: str) -> bool:
    return display_type == "reviewQuestion"

def is_displaytype_displaying_review_answer(display_type: str) -> bool:
    return display_type == "reviewAnswer"

class UIUtils(IUIUtils):
    def __init__(self, mw: AnkiQt):
        self._mw = mw

    def is_edit_current_open(self) -> bool:
        edit_current = [window for window in self._mw.app.topLevelWidgets() if isinstance(window, EditCurrent)]
        return len(edit_current) > 0

    def run_ui_action(self, callback: Callable[[], None]) -> None:
        time = timeutil.time_execution(callback)
        self.refresh()
        tooltip(f"done in {time}")

    def _get_browser(self) -> Browser:
        browser: Browser = aqt.dialogs.open('Browser', self._mw)
        self._mw.app.processEvents()
        return browser

    def refresh(self, refresh_browser:bool = True) -> None:
        from ankiutils import app

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

    def find_hypertts_button(self) -> Optional[Any]:
        """Find the HyperTTS button in the browser window by its tooltip."""

        widget_tooltips = [widget.toolTip() for widget in self._get_browser().editor.widget.findChildren(QWidget)]
        action_tooltips = [action.toolTip() for action in self._get_browser().editor.widget.actions()]



        # Look for buttons directly in the browser
        for widget in self._get_browser().findChildren(QWidget):
            if widget.toolTip().startswith("HyperTTS:"):
                return widget

        # Look for actions in toolbar (HyperTTS might add buttons as QActions)
        for action in self._get_browser().form.menuEdit.actions():
            if action.toolTip().startswith("HyperTTS:"):
                return action

        return None

    def trigger_hypertts_button(self) -> bool:
        """Find and click the HyperTTS button."""
        button = self.find_hypertts_button()

        if button is None:
            print("HyperTTS button not found")
            return False

        if isinstance(button, QPushButton):
            button.click()
            return True
        elif isinstance(button, QAction):
            button.trigger()
            return True

        return False