from typing import Callable

import aqt
from aqt import mw
from aqt.browser import Browser
from aqt.browser.previewer import Previewer
from aqt.editcurrent import EditCurrent
from aqt.reviewer import RefreshNeeded
from aqt.utils import tooltip

from ankiutils.audio_suppressor import audio_suppressor
from sysutils import timeutil


class UIUtils:
    @staticmethod
    def is_edit_current_open() -> bool:
        edit_current = [window for window in mw.app.topLevelWidgets() if isinstance(window, EditCurrent)]
        return len(edit_current) > 0

    @staticmethod
    def is_edit_current_active() -> bool:
        edit_current = [window for window in mw.app.topLevelWidgets() if isinstance(window, EditCurrent)]
        if len(edit_current) > 0:
            return edit_current[0].isActiveWindow()
        return False

    @staticmethod
    def run_ui_action(callback: Callable[[], None]) -> None:
        time = timeutil.time_execution(callback)
        UIUtils.refresh()
        tooltip(f"done in {time}")

    @staticmethod
    def refresh() -> None:
        audio_suppressor.suppress_for_seconds(.1)
        if mw.reviewer.card:
            mw.reviewer._refresh_needed = RefreshNeeded.NOTE_TEXT
            mw.reviewer.refresh_if_needed()

        previewer: list[Previewer] = [window for window in mw.app.topLevelWidgets() if isinstance(window, Previewer)]
        if len(previewer) > 0:
            previewer[0].render_card()

        browser: list[Browser] = [window for window in mw.app.topLevelWidgets() if isinstance(window, Browser)]
        if len(browser) > 0:
            browser[0].onSearchActivated()

    @staticmethod
    def show_current_review_in_preview() -> None:
        mw.onBrowse()
        UIUtils.activate_preview()
        mw.activateWindow()

    @staticmethod
    def activate_preview() -> None:
        browser: Browser = aqt.dialogs.open('Browser', aqt.mw) # noqa
        mw.app.processEvents()
        if browser._previewer is None: # noqa
            browser.onTogglePreview()
        else:
            browser._previewer.activateWindow() # noqa

    @staticmethod
    def deactivate_preview() -> None:
        browser: Browser = aqt.dialogs.open('Browser', aqt.mw) # noqa
        mw.app.processEvents()
        if browser._previewer: # noqa
            browser.onTogglePreview()

    @classmethod
    def activate_reviewer(cls) -> None:
        mw.activateWindow()
