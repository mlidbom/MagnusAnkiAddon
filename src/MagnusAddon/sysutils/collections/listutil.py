from typing import TypeVar, List, Callable

T = TypeVar('T')

def remove_duplicates_with_lambda(input_list: List[T], callback: Callable[[T], str]) -> List[T]:
    unique = set[str]()
    result = list[T]()
    for item in input_list:
        key = callback(item)
        if key not in unique:
            unique.add(key)
            result.append(item)

    return result

