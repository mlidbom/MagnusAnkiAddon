from sysutils.ex_str import full_width_space

def pad_to_length(value: str, target_length: int) -> str:
    padding = max(0, target_length - len(value))
    return value + full_width_space * padding

def is_hiragana(char: str) -> bool:
    return 0x3040 <= ord(char) <= 0x309F

def is_katakana(char: str) -> bool:
    return 0x30A0 <= ord(char) <= 0x30FF

def is_kana(char: str) -> bool:
    return is_hiragana(char) or is_katakana(char)

def get_conjugation_base(word: str) -> str:
    if word.endswith(('う', 'く', 'ぐ', 'す', 'つ', 'ぬ', 'ふ', 'む', 'る', 'い')):  # verb endings and i-adjective ending
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

#from: https://www.darrenlester.com/blog/recognising-japanese-characters-with-javascript and http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
# CJK unifed ideographs - Common and uncommon kanji ( 4e00 - 9faf)
# CJK unified ideographs Extension A - Rare kanji ( 3400 - 4dbf)

def is_kanji(ch: str) -> bool:
    ordinal = ord(ch)
    return (0x4E00 <= ordinal <= 0x9FAF or
            0x3400 <= ordinal <= 0x4DBF)

def contains_kanji(string:str) -> bool:
    return any(is_kanji(c) for c in string)

# def is_kanji(char) -> bool:
#     ordinal = ord(char)
#     return (0x4e00 <= ordinal <= 0x9faf or
#             0x3400 <= ordinal <= 0x4dbf or
#             0x20000 <= ordinal <= 0x2a6df or
#             0x2a700 <= ordinal <= 0x2b73f or
#             0x2b740 <= ordinal <= 0x2b81f or
#             0x2b820 <= ordinal <= 0x2ceaf)

def is_only_kana(word: str) -> bool:
    for char in word:
        if not is_kana(char):
            return False
    return True
