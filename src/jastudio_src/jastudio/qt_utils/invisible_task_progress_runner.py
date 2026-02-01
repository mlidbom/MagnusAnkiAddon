from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from jastudio.qt_utils.i_task_progress_runner import ITaskRunner
from jastudio.sysutils.timeutil import StopWatch

from jastudio import mylog

if TYPE_CHECKING:
    from collections.abc import Callable


class InvisibleTaskRunner(ITaskRunner, Slots):
    # noinspection PyUnusedLocal
    def __init__(self, window_title: str, label_text: str) -> None:  # pyright: ignore
        pass

    @override
    def process_with_progress[TInput, TOutput](self, items: list[TInput], process_item: Callable[[TInput], TOutput], message: str, run_gc: bool = False, minimum_items_to_gc: int = 0) -> list[TOutput]:
        result = [process_item(item) for item in items]
        total_items = len(items)
        watch = StopWatch()
        mylog.debug(f"##--InvisibleTaskRunner--## Finished {message} in {watch.elapsed_formatted()} handled {total_items} items")
        return result
    @override
    def set_label_text(self, text: str) -> None: pass  # pyright: ignore
    @override
    def close(self) -> None: pass
    @override
    def run_on_background_thread_with_spinning_progress_dialog[TResult](self, message: str, action: Callable[[], TResult]) -> TResult:  # pyright: ignore
        watch = StopWatch()
        result = action()
        mylog.debug(f"##--QtTaskProgressRunner--## Finished {message} in {watch.elapsed_formatted()}")
        return result
