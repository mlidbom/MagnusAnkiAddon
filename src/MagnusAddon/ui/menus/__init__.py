from __future__ import annotations

from . import browser, common
from . import kanji as kanji
from . import radical as radical
from . import sentence as sentence
from . import vocab as vocab
from . import web_search as web_search


def init() -> None:
    common.init()
    browser.init()
