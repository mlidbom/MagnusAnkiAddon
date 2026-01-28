from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from collections.abc import Callable


class IUIUtils(Slots):
    def is_edit_current_open(self) -> bool: raise NotImplementedError()
    def refresh(self, refresh_browser:bool = True) -> None: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def run_ui_action(self, callback: Callable[[],None]) -> None: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def activate_preview(self) -> None: raise NotImplementedError()
    def tool_tip(self, message:str, milliseconds:int = 3000) -> None: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def is_preview_open(self) -> bool: return False