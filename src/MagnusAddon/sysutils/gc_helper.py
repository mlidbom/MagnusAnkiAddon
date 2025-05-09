from __future__ import annotations

import gc
from contextlib import contextmanager
from typing import Iterator

@contextmanager
def run_with_gc_enabled_and_collect_before_disabling_again() -> Iterator[None]:
    #this may be used at multiple levels, so only do the changes if gc is currently disabled
    enabled_gc = False
    if not gc.isenabled():
        gc.enable()
        enabled_gc = True
    try:
        yield
    finally:
        if enabled_gc:
            gc.collect()
            gc.disable()
