from __future__ import annotations

import time


def sleep_thread_not_doing_the_current_work(seconds: float) -> None:
    time.sleep(seconds)