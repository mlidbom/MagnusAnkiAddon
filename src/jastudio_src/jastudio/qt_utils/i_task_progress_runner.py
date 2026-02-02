from __future__ import annotations

from typing import TYPE_CHECKING

from jaslib.sysutils.abstract_method_called_error import AbstractMethodCalledError

if TYPE_CHECKING:
    from collections.abc import Callable


class ITaskRunner:
    # noinspection Annotator
    def process_with_progress[TInput, TOutput](self, items: list[TInput], process_item: Callable[[TInput], TOutput], message: str, run_gc: bool = False, minimum_items_to_gc: int = 0) -> list[TOutput]: raise AbstractMethodCalledError()  # pyright: ignore
    # noinspection Annotator
    def set_label_text(self, text: str) -> None: raise AbstractMethodCalledError()  # pyright: ignore
    def close(self) -> None: raise AbstractMethodCalledError()
    # noinspection Annotator
    def run_on_background_thread_with_spinning_progress_dialog[TResult](self, message: str, action: Callable[[], TResult]) -> TResult: raise AbstractMethodCalledError()  # pyright: ignore
    def run_gc(self) -> None: pass
    # noinspection PyUnusedFunction
    def is_hidden(self) -> bool: return True
