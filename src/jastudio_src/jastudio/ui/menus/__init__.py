from __future__ import annotations


def init() -> None:
    from jastudio.ui.menus import browser, common
    common.init()
    browser.init()
