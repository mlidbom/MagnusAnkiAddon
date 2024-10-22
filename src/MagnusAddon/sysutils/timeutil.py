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

def format_seconds_as_hh_mm_ss(estimated_remaining_time: float) -> str:
    # Convert estimated remaining time to hours:minutes:seconds format
    hours = int(estimated_remaining_time // 3600)
    minutes = int((estimated_remaining_time % 3600) // 60)
    seconds = int(estimated_remaining_time % 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"
