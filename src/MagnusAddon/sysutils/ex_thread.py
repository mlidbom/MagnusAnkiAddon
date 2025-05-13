from time import sleep, time
from typing import Callable


class WaitTimeoutError(Exception):
    pass

def wait_until_(condition: Callable[[], bool], timeout_seconds: float = 60.0) -> None:
    start_time = time()
    while not condition():
        if time() - start_time > timeout_seconds:
            raise WaitTimeoutError(f"Timed out after {timeout_seconds} seconds")
        sleep(0.01)