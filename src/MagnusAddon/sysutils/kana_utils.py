from __future__ import annotations

import pykakasi

# noinspection PyPackageRequirements
import romkan
from sysutils import typed
from sysutils.ex_str import full_width_space

# ruff: noqa: PLR2004


def pad_to_length(value: str, target_length: int) -> str:
    padding = max(0, target_length - len(value))
    return value + full_width_space * padding

def character_is_hiragana(char: str) -> bool:
    return 0x3040 <= ord(char) <= 0x309F

def character_is_katakana(char: str) -> bool:
    return 0x30A0 <= ord(char) <= 0x30FF

def character_is_kana(char: str) -> bool:
    return character_is_hiragana(char) or character_is_katakana(char)

def hiragana_to_katakana(hiragana: str) -> str:
    def char_to_katakana(char: str) -> str:
        return chr(ord(char) + 96) if character_is_hiragana(char) else char

    return "".join([char_to_katakana(char) for char in hiragana])

def katakana_to_hiragana(katakana: str) -> str:
    def char_to_hiragana(char: str) -> str:
        return chr(ord(char) - 96) if character_is_katakana(char) else char

    return "".join([char_to_hiragana(char) for char in katakana])

# from: https://www.darrenlester.com/blog/recognising-japanese-characters-with-javascript and http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
# CJK unifed ideographs - Common and uncommon kanji ( 4e00 - 9faf)
# CJK unified ideographs Extension A - Rare kanji ( 3400 - 4dbf)

def character_is_kanji(ch: str) -> bool:
    ordinal = ord(ch)
    return (0x4E00 <= ordinal <= 0x9FAF or
            0x3400 <= ordinal <= 0x4DBF)

def contains_kanji(string: str) -> bool:
    return any(character_is_kanji(c) for c in string)

# def is_kanji(char) -> bool:
#     ordinal = ord(char)
#     return (0x4e00 <= ordinal <= 0x9faf or
#             0x3400 <= ordinal <= 0x4dbf or
#             0x20000 <= ordinal <= 0x2a6df or
#             0x2a700 <= ordinal <= 0x2b73f or
#             0x2b740 <= ordinal <= 0x2b81f or
#             0x2b820 <= ordinal <= 0x2ceaf)

def is_only_kana(text: str) -> bool:
    return not any(not character_is_kana(char) for char in text)

def is_only_hiragana(text: str) -> bool:
    return not any(not character_is_hiragana(char) for char in text)

def is_only_katakana(text: str) -> bool:
    return not any(not character_is_katakana(char) for char in text)

_kakasi = pykakasi.kakasi()  # type: ignore
def romanize(text:str) -> str:
    if text == "": return ""
    if text[-1] == "っ" or text[-1] == "ッ":
        text = text[:-1]

    result = _kakasi.convert(text)
    return "".join([item["hepburn"] for item in result])

def romaji_to_hiragana(string:str) -> str:
    return typed.str_(romkan.to_hiragana(string))

def romaji_to_katakana(string:str) -> str:
    return typed.str_(romkan.to_katakana(string))

def anything_to_hiragana(string:str) -> str:
    return katakana_to_hiragana(string) if is_only_kana(string) else romaji_to_hiragana(string)