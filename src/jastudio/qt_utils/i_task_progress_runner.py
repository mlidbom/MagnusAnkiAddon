from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class ITaskRunner:
    # noinspection DuplicatedCode,Annotator
    def process_with_progress[TInput, TOutput](self, items: list[TInput], process_item: Callable[[TInput], TOutput], message: str, run_gc: bool = False, minimum_items_to_gc: int = 0) -> list[TOutput]: raise NotImplementedError()  # pyright: ignore
    # noinspection DuplicatedCode,Annotator
    def set_label_text(self, text: str) -> None: raise NotImplementedError()  # pyright: ignore
    def close(self) -> None: raise NotImplementedError()
    # noinspection DuplicatedCode
    def run_on_background_thread_with_spinning_progress_dialog[TResult](self, message: str, action: Callable[[], TResult]) -> TResult: raise NotImplementedError()  # pyright: ignore
    def run_gc(self) -> None: pass
    # noinspection PyUnusedFunction
    def is_hidden(self) -> bool: return True
