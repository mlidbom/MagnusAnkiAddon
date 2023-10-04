"""utilities to create type safe predicates without having to define your own method to pass"""
from typing import Callable, TypeVar

T = TypeVar('T')

def eq_(entry:T) -> Callable[[T], bool]:
    def _equals(candidate:T) -> bool: return candidate == entry
    return _equals