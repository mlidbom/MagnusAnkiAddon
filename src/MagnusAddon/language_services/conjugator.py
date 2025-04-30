from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from note.vocabnote import VocabNote

_i_stem_index = 0
_a_stem_index = 1
_e_stem_index = 2
_te_stem_index = 3

_1_character_mappings: dict[str, list[str]] = {'う': ['い', 'わ', 'え', 'っ'],
                                               'く': ['き', 'か', 'け', 'い'],
                                               'ぐ': ['ぎ', 'が', 'げ', 'い'],
                                               'す': ['し', 'さ', 'せ'],
                                               'つ': ['ち', 'た', 'て', 'っ'],
                                               'ぬ': ['に', 'な', 'ね', 'ん'],
                                               'ぶ': ['び', 'ば', 'べ', 'ん'],
                                               'む': ['み', 'ま', 'め', 'ん'],
                                               'る': ['り', 'ら', 'れ', 'っ'],
                                               'い': ['く', 'け', 'か']}

_2_character_mappings: dict[str, list[str]] = {'する': ['し', 'さ', 'すれ'],
                                               'くる': ['き', 'こ', 'くれ'],
                                               'ます': ['まし', 'ませ'],
                                               'いく': ['いき', 'いか', 'いけ', 'いっ', 'いこ'],
                                               'いい': ['よく', 'よけ', 'よか'],
                                               '行く': ['行き', '行か', '行け', '行っ', '行こ']}

_aru_verbs: set[str] = {'なさる', 'くださる', 'おっしゃる', 'ござる', 'らっしゃる', '下さる', '為さる'}

_aru_mappings: dict[str, list[str]] = {'さる': ['さい', 'さら', 'され', 'さっ'],
                                       'ざる': ['ざい', 'ざら', 'ざれ', 'ざっ'],
                                       'ゃる': ['ゃい', 'ゃら', 'れば', 'ゃっ']}
def _is_aru_verb(word: str) -> bool:
    return any(aru_ending for aru_ending in _aru_verbs if word.endswith(aru_ending))

def get_word_stems(word: str, is_ichidan_verb: bool = False, is_godan: bool = False) -> list[str]:
    if _is_aru_verb(word):
        return [word[:-2] + end for end in _aru_mappings[word[-2:]]]
    if is_ichidan_verb:
        return [word[:-1]]
    if word[-2:] in _2_character_mappings:
        return [word[:-2] + end for end in _2_character_mappings[word[-2:]]]
    if word[-1] in _1_character_mappings:
        if is_godan or word[-1] != "る":
            return [word[:-1] + end for end in _1_character_mappings[word[-1]]]
        else:
            return [word[:-1] + end for end in _1_character_mappings[word[-1]]] + [word[:-1]]
    return [word]


def _get_stem(word: str, stem_index:int, is_ichidan_verb: bool = False, is_godan: bool = False) -> str:
    if _is_aru_verb(word):
        return word[:-2] + _aru_mappings[word[-2:]][stem_index]
    if is_ichidan_verb:
        return word[:-1]
    if word[-2:] in _2_character_mappings:
        return word[:-2] + _2_character_mappings[word[-2:]][stem_index]
    if word[-1] in _1_character_mappings:
        if is_godan or word[-1] != "る":
            return word[:-1] + _1_character_mappings[word[-1]][stem_index]
        else:
            return word[:-1] + _1_character_mappings[word[-1]][stem_index]
    return word


def get_i_stem(word: str, is_ichidan_verb: bool = False, is_godan: bool = False) -> str:
    return _get_stem(word, _i_stem_index, is_ichidan_verb, is_godan)

def get_a_stem(word: str, is_ichidan_verb: bool = False, is_godan: bool = False) -> str:
    return _get_stem(word, _a_stem_index, is_ichidan_verb, is_godan)

def get_e_stem(word: str, is_ichidan_verb: bool = False, is_godan: bool = False) -> str:
    return _get_stem(word, _e_stem_index, is_ichidan_verb, is_godan)

def get_te_stem(word: str, is_ichidan_verb: bool = False, is_godan: bool = False) -> str:
    return _get_stem(word, _te_stem_index, is_ichidan_verb, is_godan)

def get_masu_form(vocab:VocabNote) -> str:
    return get_i_stem(vocab.get_question(), vocab.is_ichidan_verb(), vocab.is_godan_verb()) + "ます"