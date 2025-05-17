from __future__ import annotations

from typing import Callable

from ankiutils.ui_utils_interface import IUIUtils
from autoslot import Slots


class UIUtilsStub(IUIUtils, Slots):
    def run_ui_action(self, callback: Callable[[], None]) -> None:
        callback()

    def refresh(self, refresh_browser: bool = True) -> None: pass

    def is_edit_current_open(self) -> bool: raise Exception("Unsupported by this stub")
    def activate_preview(self) -> None: raise Exception("Unsupported by this stub")

    def tool_tip(self, message: str, milliseconds: int = 3000) -> None: pass
