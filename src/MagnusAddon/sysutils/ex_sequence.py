"""extensions to the built in Sequence type"""
from typing import Sequence, TypeVar

T = TypeVar('T')

def flatten(this: Sequence[Sequence[T]]) -> list[T]:
    """`returns` all the items in `this` in order, flattened into a one dimensional list"""
    return [item for sub_list in this for item in sub_list]

def remove_duplicates_while_retaining_order(sequence:Sequence[T]) -> list[T]:
    seen = set()
    result = []
    for item in sequence:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result