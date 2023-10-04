"""extensions to the built in list type"""
from typing import Callable, TypeVar

from sysutils import ex_iterable

T = TypeVar('T')

def consume_while(predicate: Callable[[T], bool], this: list[T]) -> list[T]:
    """while `condition` is true, removes the item from `this` `return`: the removed items in order"""
    consumed = list(ex_iterable.take_while(predicate, this))
    del this[:len(consumed)]
    return consumed

def consume_until_before(predicate: Callable[[T], bool], this: list[T]) -> list[T]:
    """while `condition` is false, removes the item from `this`. `return`: the removed items in order"""
    consumed = list(ex_iterable.take_until_before(predicate, this))
    del this[:len(consumed)]
    return consumed
