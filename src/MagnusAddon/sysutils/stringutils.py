import re


newline = "\n"

class StringUtils:
    @staticmethod
    def newline() -> str: return newline

    @staticmethod
    def pad_to_length(value: str, target_length: int) -> str:
        padding = max(0, target_length - len(value))
        return value + " " * padding

    @staticmethod
    def extract_characters(string: str) -> list[str]:
        return [char for char in string if not char.isspace()]

    @staticmethod
    def extract_comma_separated_values(string: str) -> list[str]:
        return [item for item in (item.strip() for item in string.strip().split(",")) if item]

    @staticmethod
    def strip_html_and_bracket_markup(string: str) -> str:
        return re.sub('<.*?>|\[.*?\]', '', string) # noqa

    @staticmethod
    def strip_html_markup(string: str) -> str:
        return re.sub('<.*?>', '', string) # noqa


    @staticmethod
    def strip_html_and_bracket_markup_and_noise_characters(string: str) -> str:
        return re.sub('<.*?>|\[.*?\]|[〜]', '', string)  # noqa

    @staticmethod
    def remove_duplicates_characters(input_str: str) -> str:
        seen = set()
        output_str = ""
        for char in input_str:
            if char not in seen:
                seen.add(char)
                output_str += char
        return output_str


