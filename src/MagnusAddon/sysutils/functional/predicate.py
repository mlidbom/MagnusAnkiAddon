from typing import Callable, TypeVar

T = TypeVar('T')
Predicate = Callable[[T], bool]

def eq_(this: T) -> Callable[[T], bool]:
    """`returns` a predicate that returns argument == `this` """
    def _equals(candidate: T) -> bool: return candidate == this
    return _equals
