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

_word_last_character_stem_mappings:dict[str, list[str]] = {'う': ['い','わ','え'],
                                                           'く': ['き','か','け'],
                                                           'ぐ': ['ぎ','が','げ'],
                                                           'す': ['し','さ','せ'],
                                                           'つ': ['ち','た','て'],
                                                           'ぬ': ['に','な','ね'],
                                                           'ぶ': ['び','ば','べ'],
                                                           'む': ['み','ま','め'],
                                                           'る': ['り','ら','れ'],
                                                           'い': ['く']}

_irregular_verb_stem_mappings: dict[str, list[str]] = {'する': ['すれ', 'し', 'さ'],
                                                       'くる': ['くれ', 'き','こ']}
def get_highlighting_conjugation_bases(word: str, is_ichidan_verb:bool = False) -> list[str]:
    if is_ichidan_verb:
        return [word[:-1]]

    if word[-2:] in _irregular_verb_stem_mappings:
        return [word[:-2] + end for end in _irregular_verb_stem_mappings[word[-2:]]]
    if word.endswith('てくる'):  # verb endings and i-adjective ending
        return [word[:-2] + "き", word[:-2] + "こ"]
    if word[-1] in _word_last_character_stem_mappings:
        return [word[:-1] + end for end in _word_last_character_stem_mappings[word[-1]]] + [word[:-1]]
    return [word]

def to_katakana(hiragana: str) -> str:
    def char_to_katakana(char: str) -> str:
        return chr(ord(char) + 96) if is_hiragana(char) else char

    return ''.join([char_to_katakana(char) for char in hiragana])

def to_hiragana(hiragana: str) -> str:
    def char_to_hiragana(char: str) -> str:
        return chr(ord(char) - 96) if is_katakana(char) else char

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

def is_only_kana(text: str) -> bool:
    return not any(not is_kana(char) for char in text)

def is_only_hiragana(text: str) -> bool:
    return not any(not is_hiragana(char) for char in text)

def is_only_katakana(text: str) -> bool:
    return not any(not is_katakana(char) for char in text)

