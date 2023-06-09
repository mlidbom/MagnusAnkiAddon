from typing import *


class ListUtils:
    def flatten_list(the_list: List):
        return [item for sub_list in the_list for item in sub_list]


class StringUtils:
    def extract_characters(string: str):
        return [char for char in string if not char.isspace()]

    def extract_comma_separated_values(string: str) -> List:
        result = [item.strip() for item in string.split(",")]
        return [] + result