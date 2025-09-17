from __future__ import annotations

from typing import TYPE_CHECKING, override

from ankiutils.ui_utils_interface import IUIUtils
from ex_autoslot import ProfilableAutoSlots

if TYPE_CHECKING:
    from collections.abc import Callable


class UIUtilsStub(IUIUtils, ProfilableAutoSlots):
    @override
    def run_ui_action(self, callback: Callable[[], None]) -> None:
        callback()

    @override
    def refresh(self, refresh_browser: bool = True) -> None: pass
    @override
    def is_edit_current_open(self) -> bool: raise Exception("Unsupported by this stub")
    @override
    def activate_preview(self) -> None: raise Exception("Unsupported by this stub")
    @override
    def tool_tip(self, message: str, milliseconds: int = 3000) -> None: pass
