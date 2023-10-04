"""extensions to the built in Sequence type"""
from typing import Sequence, TypeVar

T = TypeVar('T')

def flatten(this: Sequence[Sequence[T]]) -> list[T]:
    """`returns` all the items in `this` in order, flattened into a one dimensional list"""
    return [item for sub_list in this for item in sub_list]