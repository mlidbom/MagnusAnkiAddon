import re
from typing import List

import aqt
from aqt import mw
from aqt.browser import Browser
from aqt.browser.previewer import Previewer
from aqt.editcurrent import EditCurrent
from aqt.reviewer import RefreshNeeded
from aqt.utils import tooltip

from sysutils import timeutil
from typing import TypeVar, Generic, Callable, Iterable

T = TypeVar('T')

class TypedList(Generic[T]):
    @staticmethod
    def any(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
        for item in iterable:
            if predicate(item):
                return True
        return False

class ListUtils:
    @staticmethod
    def any(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
        for item in iterable:
            if predicate(item):
                return True
        return False

    @staticmethod
    def flatten_list(the_list: List):
        return [item for sub_list in the_list for item in sub_list]

class StringUtils:
    @staticmethod
    def newline() -> str: return "\n"

    @staticmethod
    def backslash() -> str: return "\\"

    @staticmethod
    def extract_characters(string: str):
        return [char for char in string if not char.isspace()]

    @staticmethod
    def extract_comma_separated_values(string: str) -> list[str]:
        result = [item.strip() for item in string.split(",")]
        return [] + result

    @staticmethod
    def strip_markup(string: str) -> str:
        return re.sub('<.*?>|\[.*?\]', '', string) # noqa

    @staticmethod
    def strip_markup_and_noise_characters(string: str) -> str:
        return re.sub('<.*?>|\[.*?\]|[〜]', '', string)  # noqa


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
