from __future__ import annotations

import time


def sleep_ex(seconds: float) -> None:# all our sleep calls should go through this so we can see in profiling if we are the one's sleeping
    time.sleep(seconds)