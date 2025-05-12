"""extentions for working with Iterable"""
from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Callable, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

T = TypeVar('T')

def take_while(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Iterable[T]:
    """`returns` an iterable containing the items in `iterable` until (exclusive) `condition` returns false"""
    return itertools.takewhile(predicate, iterable)

def flatten(iterable: Iterable[Iterable[T]]) -> Iterable[T]:
    return [item for sub_list in iterable for item in sub_list]