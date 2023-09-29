from typing import TypeVar, Generic, Iterable, Callable

T = TypeVar('T')

class TypedList(Generic[T]):
    @staticmethod
    def any(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
        for item in iterable:
            if predicate(item):
                return True
        return False