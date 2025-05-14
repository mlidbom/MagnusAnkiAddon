from __future__ import annotations

from typing import TYPE_CHECKING, Callable  # noqa: I001

import aqt
from ankiutils import app

if TYPE_CHECKING:
    from aqt.browser import Browser


def do_lookup_and_show_previewer(text: str) -> None:
    do_lookup(text)
    app.get_ui_utils().activate_preview()

def do_lookup(text: str) -> None:
    browser: Browser = aqt.dialogs.open("Browser", aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()
    app.get_ui_utils().activate_preview()

def lookup_promise(search: Callable[[], str]) -> Callable[[], None]: return lambda: do_lookup(search())

def lookup_and_show_previewer_promise(search: Callable[[], str]) -> Callable[[], None]: return lambda: do_lookup_and_show_previewer(search())
