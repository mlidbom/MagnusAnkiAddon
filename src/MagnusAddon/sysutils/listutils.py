from typing import Iterable, TypeVar, Callable, Sequence

T = TypeVar('T')

class ListUtils:
    @staticmethod
    def any(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
        for item in iterable:
            if predicate(item):
                return True
        return False

    @staticmethod
    def flatten_list(the_list: Sequence[Sequence[T]]) -> list[T]:
        return [item for sub_list in the_list for item in sub_list]