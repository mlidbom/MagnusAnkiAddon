from __future__ import annotations

from . import browser, common
from . import notes as notes
from . import web_search as web_search


def init() -> None:
    common.init()
    browser.init()
