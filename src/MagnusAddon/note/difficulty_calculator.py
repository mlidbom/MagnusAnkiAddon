from sysutils import ex_sequence, kana_utils

KANJI_WEIGHT = 4
KATAKANA_WEIGHT = 1.5

def find_difficulty(string: str) -> int:
    kanji_characters = ex_sequence.count(string, kana_utils.is_kanji)
    katakana_characters = ex_sequence.count(string, kana_utils.is_katakana)
    hiragana_characters = ex_sequence.count(string, kana_utils.is_hiragana)
    return int(kanji_characters * KANJI_WEIGHT + katakana_characters * KATAKANA_WEIGHT + hiragana_characters)

class DifficultyCalculator:
    def __init__(self, levels: list[int], difficulties: list[float]) -> None:
        self.levels = levels
        self.difficulties = difficulties

    def find_level(self, string: str) -> int:
        difficulty = find_difficulty(string)
        if difficulty <= self.difficulties[0]: return self.levels[0]
        for level in self.levels[1:]:
            if self.difficulties[level - 2] < difficulty <= self.difficulties[level - 1]:
                return level
        return self.levels[-1]