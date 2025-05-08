from typing import Callable

import aqt
from aqt.browser import Browser  # type: ignore

from ankiutils import app

def do_lookup_and_show_previewer(text: str) -> None:
    do_lookup(text)
    app.ui_utils().activate_preview()

def do_lookup(text: str) -> None:
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)  # type: ignore
    browser.onSearchActivated()
    app.ui_utils().activate_preview()

def lookup_promise(search: Callable[[], str]) -> Callable[[], None]: return lambda: do_lookup(search())

def lookup_and_show_previewer_promise(search: Callable[[], str]) -> Callable[[], None]: return lambda: do_lookup_and_show_previewer(search())
