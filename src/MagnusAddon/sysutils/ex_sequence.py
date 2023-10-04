from typing import Callable, TypeVar, Sequence

T = TypeVar('T')

def flatten(the_list: Sequence[Sequence[T]]) -> list[T]:
    return [item for sub_list in the_list for item in sub_list]

def count_while(the_list: Sequence[T], condition: Callable[[T], bool]) -> int:
    return next((index for index, item in enumerate(the_list) if not condition(item)), len(the_list))

def count_until(the_list: Sequence[T], condition: Callable[[T], bool]) -> int:
    return next((index for index, item in enumerate(the_list) if condition(item)), len(the_list))