from typing import *
import re

from aqt import *
from aqt.browser import Browser
from aqt.browser.previewer import Previewer
from aqt.reviewer import *
from aqt.webview import *


class ListUtils:
    def flatten_list(the_list: List):
        return [item for sub_list in the_list for item in sub_list]


class StringUtils:
    def Newline() -> str: return "\n"
    def Backslash() -> str: return "\\"

    def extract_characters(string: str):
        return [char for char in string if not char.isspace()]

    def extract_comma_separated_values(string: str) -> List:
        result = [item.strip() for item in string.split(",")]
        return [] + result

    def strip_markup(string:str) -> str:
        return re.sub('<.*?>', '', string)

class UIUtils:
    def refresh() -> None:
        if mw.reviewer:
            mw.reviewer._refresh_needed = RefreshNeeded.NOTE_TEXT
            mw.reviewer.refresh_if_needed()

        previewer: list[Previewer] = [window for window in mw.app.topLevelWidgets() if isinstance(window, Previewer)]
        if len(previewer) > 0:
            previewer[0].render_card()

        browser: list[Browser] = [window for window in mw.app.topLevelWidgets() if isinstance(window, Browser)]
        if len(browser) > 0:
            browser[0].onSearchActivated()


