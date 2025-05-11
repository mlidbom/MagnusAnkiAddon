"""extentions for working with Iterable"""
import itertools
from collections.abc import Iterable
from typing import Callable, TypeVar

T = TypeVar('T')

def take_while(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Iterable[T]:
    """`returns` an iterable containing the items in `iterable` until (exclusive) `condition` returns false"""
    return itertools.takewhile(predicate, iterable)

def flatten(iterable: Iterable[Iterable[T]]) -> Iterable[T]:
    return [item for sub_list in iterable for item in sub_list]