from sysutils import ex_sequence, kana_utils

KANJI_WEIGHT = 4.0
KATAKANA_WEIGHT = 1.5

def find_difficulty(string: str) -> float:
    kanji_characters = ex_sequence.count(string, kana_utils.is_kanji)
    katakana_characters = ex_sequence.count(string, kana_utils.is_katakana)
    hiragana_characters = ex_sequence.count(string, kana_utils.is_hiragana)
    return kanji_characters * KANJI_WEIGHT + katakana_characters * KATAKANA_WEIGHT + hiragana_characters

class DifficultyCalculator:
    def __init__(self, starting_seconds:float, hiragana_seconds:float, katakata_weight:float, kanji_weight:float) -> None:
        self.starting_seconds = starting_seconds
        self.hiragana_seconds = hiragana_seconds
        self.katakata_weight = katakata_weight
        self.kanji_weight = kanji_weight

    def allowed_seconds(self, string:str) -> float:
        hiragana_seconds = ex_sequence.count(string, kana_utils.is_hiragana) * self.hiragana_seconds
        katakana_seconds = ex_sequence.count(string, kana_utils.is_katakana) * self.hiragana_seconds * self.katakata_weight
        kanji_seconds = ex_sequence.count(string, kana_utils.is_kanji) * self.hiragana_seconds * self.kanji_weight

        return self.starting_seconds + hiragana_seconds + katakana_seconds + kanji_seconds