from __future__ import annotations

from typing import Callable, TypeVar

TResult: TypeVar = TypeVar("TResult")
TParam1 = TypeVar("TParam1")
TParam2 = TypeVar("TParam2")
TParam3 = TypeVar("TParam3")
TParam4 = TypeVar("TParam4")

def bind1(func: Callable[[TParam1], TResult], param: TParam1) -> Callable[[], TResult]:
    return lambda: func(param)

def bind2(func: Callable[[TParam1, TParam2], TResult], p1: TParam1, p2: TParam2) -> Callable[[], TResult]:
    return lambda: func(p1, p2)

def bind3(func: Callable[[TParam1, TParam2, TParam3], TResult], p1: TParam1, p2: TParam2, p3: TParam3) -> Callable[[], TResult]:
    return lambda: func(p1, p2, p3)

def bind4(func: Callable[[TParam1, TParam2, TParam3, TParam4], TResult], p1: TParam1, p2: TParam2, p3: TParam3, p4: TParam4) -> Callable[[], TResult]:
    return lambda: func(p1, p2, p3, p4)
