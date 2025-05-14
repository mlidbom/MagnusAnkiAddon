from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QMenu


class ExQmenu:
    @classmethod
    def disable_empty_submenus(cls, menu: QMenu) -> None:
        if not isinstance(menu, QMenu):
            return

        for action in menu.actions():
            submenu:Optional[QMenu] = action.menu()
            if submenu:
                cls.disable_empty_submenus(submenu)

                if len(submenu.actions()) == 0:
                    action.setEnabled(False)
