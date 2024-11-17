from __future__ import annotations
import time
from contextlib import contextmanager
from typing import Callable, Iterator

import mylog

SECONDS_PER_DAY = 24 * 60 * 60
MILLISECONDS_PER_SECOND = 1000

def time_execution(callback: Callable[[], None]) -> str:
    start_time = time.time()
    callback()
    elapsed_time = time.time() - start_time
    seconds = int(elapsed_time)
    milliseconds = int((elapsed_time - seconds) * 1000)
    return f"{seconds}:{milliseconds:03}"

def format_seconds_as_hh_mm_ss(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = int(seconds % 60)
    return f'{hours:02}:{minutes:02}:{sec:02}'

def format_seconds_as_ss_ttt_ttt(seconds: float) -> str:
    total_milliseconds = int(seconds * 1000)  # Convert seconds to milliseconds
    seconds_part = total_milliseconds // 1000  # Extract the integer part of seconds
    milliseconds_part = total_milliseconds % 1000  # Extract the milliseconds part
    microseconds_part = int((seconds - seconds_part) * 1_000_000)  # Calculate microseconds

    return f'{seconds_part}.{milliseconds_part:03d} {microseconds_part:03d}'

# noinspection PyUnusedFunction
def start_stop_watch() -> StopWatch:
    return StopWatch()

# noinspection PyUnusedFunction
class StopWatch:
    def __init__(self) -> None:
        self.start_time = time.perf_counter()

    def elapsed_seconds(self) -> float:
        return time.perf_counter() - self.start_time

    def elapsed_formatted(self) -> str:
        return format_seconds_as_ss_ttt_ttt(time.perf_counter() - self.start_time)

    @staticmethod
    @contextmanager
    def log_warning_if_slower_than(message:str, warn_if_slower_than:float) -> Iterator[None]:
        watch = StopWatch()
        try:
            yield
        finally:
            elapsed_seconds = watch.elapsed_seconds()
            message = f"Execution time:{watch.elapsed_formatted()} for {message}"
            if elapsed_seconds > warn_if_slower_than:
                mylog.log.warning(message)
            else:
                mylog.log.debug(message)
