from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

def bind1[TParam1, TResult](func: Callable[[TParam1], TResult], param: TParam1) -> Callable[[], TResult]:
    return lambda: func(param)

def bind2[TParam1, TParam2, TResult](func: Callable[[TParam1, TParam2], TResult], p1: TParam1, p2: TParam2) -> Callable[[], TResult]:
    return lambda: func(p1, p2)

def bind3[TParam1, TParam2, TParam3, TResult](func: Callable[[TParam1, TParam2, TParam3], TResult], p1: TParam1, p2: TParam2, p3: TParam3) -> Callable[[], TResult]:
    return lambda: func(p1, p2, p3)

def bind4[TParam1, TParam2, TParam3, TParam4, TResult](func: Callable[[TParam1, TParam2, TParam3, TParam4], TResult], p1: TParam1, p2: TParam2, p3: TParam3, p4: TParam4) -> Callable[[], TResult]:
    return lambda: func(p1, p2, p3, p4)
