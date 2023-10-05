from abc import ABCMeta, abstractmethod
from typing import Callable

class IUIUtils(metaclass=ABCMeta):
    @abstractmethod
    def is_edit_current_open(self) -> bool: pass

    @abstractmethod
    def is_edit_current_active(self) -> bool: pass

    @abstractmethod
    def refresh(self) -> None: pass

    @abstractmethod
    def run_ui_action(self, callback: Callable[[],None]) -> None: pass

    @abstractmethod
    def activate_preview(self) -> None: pass

    @abstractmethod
    def show_current_review_in_preview(self) -> None: pass

    @abstractmethod
    def deactivate_preview(self) -> None: pass

    @abstractmethod
    def activate_reviewer(self) -> None: pass
