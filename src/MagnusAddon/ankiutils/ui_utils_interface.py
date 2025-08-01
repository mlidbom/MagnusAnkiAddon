from __future__ import annotations

from typing import Callable

from autoslot import Slots


class IUIUtils(Slots):
    def is_edit_current_open(self) -> bool: raise NotImplementedError()
    def refresh(self, refresh_browser:bool = True) -> None: raise NotImplementedError()
    def run_ui_action(self, callback: Callable[[],None]) -> None: raise NotImplementedError()
    def activate_preview(self) -> None: raise NotImplementedError()
    def tool_tip(self, message:str, milliseconds:int = 3000) -> None: raise NotImplementedError()