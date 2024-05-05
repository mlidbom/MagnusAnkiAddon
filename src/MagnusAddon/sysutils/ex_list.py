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

def remove_items_where(predicate: Predicate[TItem], this: list[TItem]) -> list[TItem]:
    """while `condition` is true, removes the item from `this`. `return`: the removed items in order"""
    removed_items: list[TItem] = []
    index: int = 0  # index to keep track of the current position
    while index < len(this):
        item: TItem = this[index]
        if predicate(item):
            removed_items.append(this.pop(index))  # remove item and add to removed_items
        else:
            index += 1  # only increment index if item was not removed to prevent skipping
    return removed_items


def where(predicate: Predicate[TItem], this: list[TItem]) -> list[TItem]:
    return [item for item in this if predicate(item)]

def single(this: list[TItem]) -> TItem:
    assert len(this) == 1, "List must contain exactly one item"
    return this[0]