from typing import TypeVar, Sequence

T = TypeVar('T')

def flatten(the_list: Sequence[Sequence[T]]) -> list[T]:
    return [item for sub_list in the_list for item in sub_list]