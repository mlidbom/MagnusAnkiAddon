from sysutils import kana_utils


class ParsedWord:
    def __init__(self, word: str, parts_of_speech: str) -> None:
        self.word = word
        self.parts_of_speech = parts_of_speech

    def is_kana_only(self) -> bool: return kana_utils.is_only_kana(self.word)

    def __str__(self) -> str:
        return f"'{self.word}', '{self.parts_of_speech}'"

    def __eq__(self, other: any) -> bool:
        if isinstance(other, ParsedWord):
            return self.word == other.word and self.parts_of_speech == other.parts_of_speech
        return False

    def __hash__(self) -> int:
        return hash((self.word, self.parts_of_speech))