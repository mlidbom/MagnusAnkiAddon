from __future__ import annotations

from time import sleep

from line_profiling_hacks import profile_lines


@profile_lines
def wait() -> None:
    for _i in range(2):
        sleep(1)


wait()