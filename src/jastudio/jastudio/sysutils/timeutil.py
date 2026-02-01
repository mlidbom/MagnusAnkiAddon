from __future__ import annotations

import sys
import time
from contextlib import contextmanager
from typing import TYPE_CHECKING

import mylog
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

from jastudio.sysutils import typed
from jastudio.sysutils.time_span import TimeSpan

if TYPE_CHECKING:
    from collections.abc import Iterator

    from jastudio.sysutils.standard_type_aliases import Action

SECONDS_PER_DAY = 24 * 60 * 60
MILLISECONDS_PER_SECOND = 1000

def time_execution(callback: Action) -> str:
    start_time = time.time()
    callback()
    span = TimeSpan(time.time() - start_time)
    return f"{span.seconds}:{span.milliseconds:03}"

def format_seconds_as_hh_mm_ss(seconds: float) -> str:
    return TimeSpan(seconds).format_as_hh_mm_ss()

# noinspection PyUnusedFunction
def start_stop_watch() -> StopWatch:
    return StopWatch()

# noinspection PyUnusedFunction
class StopWatch(Slots):
    def __init__(self) -> None:
        self.start_time: float = time.perf_counter()

    def elapsed(self) -> TimeSpan:
        return TimeSpan(time.perf_counter() - self.start_time)

    def elapsed_seconds(self) -> float:
        return self.elapsed().total_seconds

    def elapsed_formatted(self) -> str:
        return self.elapsed().auto_format()

    @classmethod
    @contextmanager
    def log_warning_if_slower_than(cls, warn_if_slower_than:float, message:str = "") -> Iterator[None]:
        # noinspection DuplicatedCode
        watch = StopWatch()

        def get_caller_info() -> str:
            caller_frame = sys._getframe(4) # noqa  # pyright: ignore[reportPrivateUsage]
            module_name = typed.str_(caller_frame.f_globals["__name__"])  # pyright: ignore[reportAny]
            function_name = caller_frame.f_code.co_name
            return f"{module_name}..{function_name}"

        def get_message() -> str:
            return f"############## Execution time:{watch.elapsed().auto_format()} for {get_caller_info()}#{message} ##############"
        try:
            yield
        finally:
            elapsed = watch.elapsed()
            if elapsed.total_seconds > warn_if_slower_than:
                mylog.warning(get_message())
            elif elapsed.total_seconds * 2 > warn_if_slower_than:
                mylog.info(get_message())

    @classmethod
    @contextmanager
    def log_execution_time(cls, message:str = "") -> Iterator[None]:
        # noinspection DuplicatedCode
        watch = StopWatch()

        def get_caller_info() -> str:
            caller_frame = sys._getframe(4) # noqa  # pyright: ignore[reportPrivateUsage]
            module_name:str = typed.str_(caller_frame.f_globals["__name__"])  # pyright: ignore[reportAny]
            function_name = caller_frame.f_code.co_name
            return f"{module_name}..{function_name}"

        def get_message() -> str:
            return f"############## Execution time:{watch.elapsed().auto_format()} for {get_caller_info()}#{message} ##############"
        try:
            yield
        finally:
            mylog.info(get_message())
