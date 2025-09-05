from __future__ import annotations

from ui import editor_buttons, garbage_collection_fixes, hooks, menus, timing_hacks, tools_menu, web


def init() -> None:
    hooks.init()
    timing_hacks.init()
    tools_menu.init()
    web.init()
    menus.init()
    editor_buttons.init()
    garbage_collection_fixes.init()
