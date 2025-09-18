from __future__ import annotations

from typing import TYPE_CHECKING

from ex_autoslot import AutoSlots

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QMenu


class ExQmenu(AutoSlots):
    @classmethod
    def disable_empty_submenus(cls, menu: QMenu | None) -> None:
        if menu is None:
            return

        for action in menu.actions():
            submenu: QMenu | None = action.menu()  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            if submenu:
                cls.disable_empty_submenus(submenu)  # pyright: ignore[reportUnknownArgumentType]

                if len(submenu.actions()) == 0: # Disable submenu if it's empty  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
                    action.setEnabled(False)
                else: # Disable submenu if all its actions are disabled
                    all_disabled = True
                    for submenu_action in submenu.actions():  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                        if submenu_action.isEnabled():  # pyright: ignore[reportUnknownMemberType]
                            all_disabled = False
                            break
                    if all_disabled:
                        action.setEnabled(False)