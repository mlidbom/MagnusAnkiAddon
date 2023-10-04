"""utilities to create type safe predicates without having to define your own method to pass"""
from typing import Callable, TypeVar

T = TypeVar('T')

def eq_(this:T) -> Callable[[T], bool]:
    """`returns` a predicate that returns argument == `this` """
    def _equals(candidate:T) -> bool: return candidate == this
    return _equals