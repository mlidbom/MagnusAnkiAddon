from typing import Callable

import aqt
from aqt import AnkiQt  # type: ignore
from aqt.browser import Browser  # type: ignore
from aqt.browser.previewer import Previewer
from aqt.editcurrent import EditCurrent
from aqt.reviewer import RefreshNeeded
from aqt.utils import tooltip

from ankiutils.audio_suppressor import audio_suppressor
from ankiutils.ui_utils_interface import IUIUtils
from sysutils import timeutil

_ANSWER_DISPLAY_TYPES = {'reviewAnswer', 'previewAnswer', 'clayoutAnswer'}

def is_displaytype_displaying_answer(display_type: str) -> bool:
    return display_type in _ANSWER_DISPLAY_TYPES

class UIUtils(IUIUtils):
    def __init__(self, mw: AnkiQt):
        self._mw = mw

    def is_edit_current_open(self) -> bool:
        edit_current = [window for window in self._mw.app.topLevelWidgets() if isinstance(window, EditCurrent)]
        return len(edit_current) > 0

    def is_edit_current_active(self) -> bool:
        edit_current = [window for window in self._mw.app.topLevelWidgets() if isinstance(window, EditCurrent)]
        if len(edit_current) > 0:
            return edit_current[0].isActiveWindow()
        return False

    def run_ui_action(self, callback: Callable[[], None]) -> None:
        time = timeutil.time_execution(callback)
        self.refresh()
        tooltip(f"done in {time}")

    def refresh(self, refresh_browser:bool = True) -> None:
        from ankiutils import app
        app.col().flush_cache_updates()
        audio_suppressor.suppress_for_seconds(.3)
        if self._mw.reviewer.card:
            self._mw.reviewer._refresh_needed = RefreshNeeded.NOTE_TEXT
            self._mw.reviewer.refresh_if_needed()

        previewer: list[Previewer] = [window for window in self._mw.app.topLevelWidgets() if isinstance(window, Previewer)]
        if len(previewer) > 0:
            previewer[0].render_card()

        if refresh_browser:
            browser: list[Browser] = [window for window in self._mw.app.topLevelWidgets() if isinstance(window, Browser)]
            if len(browser) > 0:
                browser[0].onSearchActivated()

    def show_current_review_in_preview(self) -> None:
        self._mw.onBrowse()
        self.activate_preview()
        self._mw.activateWindow()

    def activate_preview(self) -> None:
        browser: Browser = aqt.dialogs.open('Browser', self._mw) # noqa
        self._mw.app.processEvents()
        if browser._previewer is None: # noqa
            browser.onTogglePreview()
        else:
            browser._previewer.activateWindow() # noqa

    def deactivate_preview(self) -> None:
        browser: Browser = aqt.dialogs.open('Browser', self._mw) # noqa
        self._mw.app.processEvents()
        if browser._previewer: # noqa
            browser.onTogglePreview()

    def activate_reviewer(self) -> None:
        self._mw.activateWindow()
