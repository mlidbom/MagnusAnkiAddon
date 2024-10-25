from __future__ import annotations
import time
from typing import Callable


SECONDS_PER_DAY = 24 * 60 * 60
MILLISECONDS_PER_SECOND = 1000

def one_second_from_now() -> int: return int(time.time()) + 1

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

def format_seconds_as_hh_mm_ss_ttt(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f'{hours:02}:{minutes:02}:{sec:02} {milliseconds:03}'

def start_stop_watch() -> StopWatch:
    return StopWatch()

class StopWatch:
    def __init__(self) -> None:
        self.start_time = time.time()

    def elapsed_seconds(self) -> float:
        return time.time() - self.start_time

    def elapsed_formatted(self) -> str:
        return format_seconds_as_hh_mm_ss_ttt(time.time() - self.start_time)