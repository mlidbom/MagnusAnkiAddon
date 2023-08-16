
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

def hiragana_to_katakana(hiragana: str) -> str:
    def convert_character(char: str) -> str:
        if 0x3040 <= ord(char) <= 0x309F: #is it hiragana?
            return chr(ord(char) + 96)
        else:
            return char  # Return the original character if it's not Hiragana

    return ''.join([convert_character(char) for char in hiragana])


def is_only_kana(word: str) -> bool:
    for char in word:
        if not is_kana(char):
            return False
    return True
