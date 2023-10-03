from typing import Callable

from ankiutils.ui_utils_interface import UIUtilsInterface


class UIUtilsStub(UIUtilsInterface):
    def run_ui_action(self, callback: Callable[[], None]) -> None:
        callback()

    def is_edit_current_open(self) -> bool: raise Exception("Unsupported by this stub")
    def is_edit_current_active(self) -> bool: raise Exception("Unsupported by this stub")
    def refresh(self) -> None: raise Exception("Unsupported by this stub")
    def activate_preview(self) -> None: raise Exception("Unsupported by this stub")
    def show_current_review_in_preview(self) -> None: raise Exception("Unsupported by this stub")
    def deactivate_preview(self) -> None: raise Exception("Unsupported by this stub")
    def activate_reviewer(self) -> None: raise Exception("Unsupported by this stub")
