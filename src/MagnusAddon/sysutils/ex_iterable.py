"""extentions for working with Iterable"""
import itertools
from typing import Callable, Iterable, TypeVar
T = TypeVar('T')


def count(iterable:Iterable[T]) -> int:
    """the number of items in the iterable."""
    return sum(1 for _ in iterable)

def take_until_before(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Iterable[T]:
    """`returns` an iterable containing the items in `iterable` until (exclusive) `condition` returns true"""
    def inverted_condition(item:T) -> bool: return not predicate(item)
    return itertools.takewhile(inverted_condition, iterable)

def take_until_including(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Iterable[T]:
    """`returns` an iterable containing the items in `iterable` until and including the first item when `condition` returns true"""
    for item in iterable:
        yield item
        if predicate(item):
            break

def take_while(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Iterable[T]:
    """`returns` an iterable containing the items in `iterable` until (exclusive) `condition` returns false"""
    return itertools.takewhile(predicate, iterable)

def flatten(iterable: Iterable[Iterable[T]]) -> Iterable[T]:
    return [item for sub_list in iterable for item in sub_list]