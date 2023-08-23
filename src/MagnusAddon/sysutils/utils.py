import re
from typing import List

from typing import TypeVar, Generic, Callable, Iterable

T = TypeVar('T')

class TypedList(Generic[T]):
    @staticmethod
    def any(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
        for item in iterable:
            if predicate(item):
                return True
        return False

class ListUtils:
    @staticmethod
    def any(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
        for item in iterable:
            if predicate(item):
                return True
        return False

    @staticmethod
    def flatten_list(the_list: List):
        return [item for sub_list in the_list for item in sub_list]

class StringUtils:
    @staticmethod
    def newline() -> str: return "\n"

    @staticmethod
    def backslash() -> str: return "\\"

    @staticmethod
    def extract_characters(string: str):
        return [char for char in string if not char.isspace()]

    @staticmethod
    def extract_comma_separated_values(string: str) -> list[str]:
        result = [item.strip() for item in string.split(",")]
        return [] + result

    @staticmethod
    def strip_markup(string: str) -> str:
        return re.sub('<.*?>|\[.*?\]', '', string) # noqa

    @staticmethod
    def strip_markup_and_noise_characters(string: str) -> str:
        return re.sub('<.*?>|\[.*?\]|[〜]', '', string)  # noqa


