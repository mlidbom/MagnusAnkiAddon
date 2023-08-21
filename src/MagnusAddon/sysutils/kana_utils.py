def pad_to_length(value: str, target_length: int) -> str:
    padding = max(0, target_length - len(value))
    return value + full_width_space() * padding

def full_width_space() -> str: return '　'

def is_hiragana(char:str) -> bool:
    return 0x3040 <= ord(char) <= 0x309F

def is_katakana(char:str) -> bool:
    return 0x30A0 <= ord(char) <= 0x30FF

def is_kana(char: str) -> bool:
    return is_hiragana(char) or is_katakana(char)

def strip_last_hiragana(word: str) -> str:
    if is_hiragana(word[-1]):
        return word[:-1]
    return word

def get_conjugation_base_rough(word) -> str:
    return strip_last_hiragana(word)

def get_conjugation_base(word) -> str:
    if word.endswith(('う', 'く', 'ぐ', 'す', 'つ', 'ぬ', 'ふ', 'む', 'る', 'い')): #verb endings and i-adjective ending
        return word[:-1]
    return word

def to_katakana(hiragana: str) -> str:
    def char_to_katakana(char: str) -> str:
        if is_hiragana(char):
            return chr(ord(char) + 96)
        else:
            return char

    return ''.join([char_to_katakana(char) for char in hiragana])

def to_hiragana(hiragana: str) -> str:
    def char_to_hiragana(char: str) -> str:
        if is_katakana(char):
            return chr(ord(char) - 96)
        else:
            return char

    return ''.join([char_to_hiragana(char) for char in hiragana])


def is_only_kana(word: str) -> bool:
    for char in word:
        if not is_kana(char):
            return False
    return True
