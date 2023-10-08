"""extensions to the built in list type"""
from typing import TypeVar

from sysutils import ex_iterable
from sysutils.functional.predicate import Predicate

TItem = TypeVar('TItem')

def consume_while(predicate: Predicate[TItem], this: list[TItem]) -> list[TItem]:
    """while `condition` is true, removes the item from `this` `return`: the removed items in order"""
    consumed = list(ex_iterable.take_while(predicate, this))
    del this[:len(consumed)]
    return consumed

def consume_until_before(predicate: Predicate[TItem], this: list[TItem]) -> list[TItem]:
    """while `condition` is false, removes the item from `this`. `return`: the removed items in order"""
    consumed = list(ex_iterable.take_until_before(predicate, this))
    del this[:len(consumed)]
    return consumed

def consume_until_and_including(predicate: Predicate[TItem], this: list[TItem]) -> list[TItem]:
    """while `condition` is false, removes the item from `this`. `return`: the removed items in order"""
    consumed = list(ex_iterable.take_until_including(predicate, this))
    del this[:len(consumed)]
    return consumed

def where(predicate: Predicate[TItem], this: list[TItem]) -> list[TItem]:
    return [item for item in this if predicate(item)]
