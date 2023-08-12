from typing import *

from aqt import *
from aqt.browser import Browser
from aqt.browser.previewer import Previewer
from aqt.editcurrent import EditCurrent
from aqt.reviewer import *
from aqt.webview import *


class ListUtils:
    @staticmethod
    def flatten_list(the_list: List):
        return [item for sub_list in the_list for item in sub_list]

class StringUtils:
    @staticmethod
    def Newline() -> str: return "\n"

    @staticmethod
    def Backslash() -> str: return "\\"

    @staticmethod
    def extract_characters(string: str):
        return [char for char in string if not char.isspace()]

    @staticmethod
    def extract_comma_separated_values(string: str) -> List:
        result = [item.strip() for item in string.split(",")]
        return [] + result

    @staticmethod
    def strip_markup(string:str) -> str:
        return re.sub('<.*?>', '', string)

class UIUtils:
    @staticmethod
    def is_edit_current_active():
        edit_current = [window for window in mw.app.topLevelWidgets() if isinstance(window, EditCurrent)]
        if len(edit_current) > 0:
            return edit_current[0].isActiveWindow()
        return False

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
    def show_current_review_in_preview():
        mw.onBrowse()
        UIUtils.activate_preview()
        mw.activateWindow()

    @staticmethod
    def activate_preview():
        browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
        mw.app.processEvents()
        if browser._previewer is None:
            browser.onTogglePreview()
        else:
            browser._previewer.activateWindow()