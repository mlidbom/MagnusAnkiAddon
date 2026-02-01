from __future__ import annotations

from typing import TYPE_CHECKING

import aqt
from jastudio.ankiutils import app
from jastudio.sysutils.typed import non_optional

if TYPE_CHECKING:
    from collections.abc import Callable

    from aqt.browser import Browser  # type: ignore[attr-defined]  # pyright: ignore[reportPrivateImportUsage]


def do_lookup_and_show_previewer(text: str) -> None:
    do_lookup(text)
    app.get_ui_utils().activate_preview()

def do_lookup(text: str) -> None:
    browser: Browser = aqt.dialogs.open("Browser", aqt.mw)  # pyright: ignore[reportAny]
    non_optional(browser.form.searchEdit.lineEdit()).setText(text)
    browser.onSearchActivated()  # pyright: ignore[reportUnknownMemberType]
    app.get_ui_utils().activate_preview()

def lookup_promise(search: Callable[[], str]) -> Callable[[], None]: return lambda: do_lookup(search())

def lookup_and_show_previewer_promise(search: Callable[[], str]) -> Callable[[], None]: return lambda: do_lookup_and_show_previewer(search())
