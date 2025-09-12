from __future__ import annotations

from autoslot import Slots
from PyQt6.QtWidgets import QMenu


class ExQmenu(Slots):
    @classmethod
    def disable_empty_submenus(cls, menu: QMenu | None) -> None:
        if menu is None:
            return

        for action in menu.actions():
            submenu: QMenu | None = action.menu()
            if submenu:
                cls.disable_empty_submenus(submenu)

                if len(submenu.actions()) == 0: # Disable submenu if it's empty
                    action.setEnabled(False)
                else: # Disable submenu if all its actions are disabled
                    all_disabled = True
                    for submenu_action in submenu.actions():
                        if submenu_action.isEnabled():
                            all_disabled = False
                            break
                    if all_disabled:
                        action.setEnabled(False)