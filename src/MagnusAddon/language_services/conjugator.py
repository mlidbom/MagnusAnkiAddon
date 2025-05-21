from __future__ import annotations

from typing import TYPE_CHECKING

import mylog

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

_ichidan_endings = ["", "ろ", "な"]

_godan_ru_endings = ["り", "ら", "れ", "っ"]
_godan_ru_or_ichidan_endings = _godan_ru_endings + _ichidan_endings

godan_potential_verb_ending_to_dictionary_form_endings: dict[str, str] = {"える": "う", "ける": "く", "げる": "ぐ", "せる": "す", "てる": "つ", "ねる": "ぬ", "べる": "ぶ", "める": "む", "れる": "る"}

e_stem_hiragana: set[str] = {"え", "け", "げ", "せ", "て", "ね", "べ", "め", "れ"}
e_stem_katakana: set[str] = {"エ", "ケ", "ゲ", "セ", "テ", "ネ", "ベ", "メ", "レ"}
e_stem_characters: set[str] = e_stem_hiragana | e_stem_katakana

a_stem_hiragana: set[str] = {"わ", "か", "が", "さ", "た", "な", "ば", "ま", "ら", }
a_stem_katakana: set[str] = {"ワ", "カ", "ガ", "サ", "タ", "ナ", "バ", "マ", "ラ"}
a_stem_characters: set[str] = a_stem_hiragana | a_stem_katakana

# o_row_hiragana: set[str] = {"を", "こ", "ご", "そ", "と", "の", "ぼ", "も", "ろ"}
# o_row_katakana: set[str] = {"オ", "コ", "ゴ", "ソ", "ト", "ノ", "ボ", "モ", "ロ"}
# passive_form_stem_characters: set[str] = a_stem_characters - {"な", "ナ"} # in practice な only brings false positives when searching for passive since passive ぬ verb usages are non-existent

_i_stem_index = 0
_a_stem_index = 1
_e_stem_index = 2
_te_stem_index = 3
_1_character_mappings: dict[str, list[str]] = {"う": ["い", "わ", "え", "っ"],
                                               "く": ["き", "か", "け", "い"],
                                               "ぐ": ["ぎ", "が", "げ", "い"],
                                               "す": ["し", "さ", "せ", "し"],
                                               "つ": ["ち", "た", "て", "っ"],
                                               "ぬ": ["に", "な", "ね", "ん"],
                                               "ぶ": ["び", "ば", "べ", "ん"],
                                               "む": ["み", "ま", "め", "ん"],
                                               "る": _godan_ru_endings,
                                               "い": ["く", "け", "か"]}

_2_character_mappings: dict[str, list[str]] = {"する": ["し", "さ", "すれ", "し", "せ"],
                                               "くる": ["き", "こ", "くれ", "き"],
                                               "いく": ["いき", "いか", "いけ", "いっ", "いこ"],
                                               "行く": ["行き", "行か", "行け", "行っ", "行こ"],
                                               "ます": ["まし", "ませ"],
                                               "いい": ["よく", "よけ", "よか", "よかっ"]}

_masu_forms_by_index = ["まし", "ませ", "まし", "まし"]  # not to sure about these. To say the least....

_aru_verbs: set[str] = {"なさる", "くださる", "おっしゃる", "ござる", "らっしゃる", "下さる", "為さる"}

_aru_mappings: dict[str, list[str]] = {"さる": ["さい", "さら", "され", "さっ"],
                                       "ざる": ["ざい", "ざら", "ざれ", "ざっ"],
                                       "ゃる": ["ゃい", "ゃら", "れば", "ゃっ"]}

def construct_root_verb_for_possibly_potential_godan_verb_dictionary_form(potential_verb_form: str) -> str:
    return potential_verb_form[:-2] + godan_potential_verb_ending_to_dictionary_form_endings[potential_verb_form[-2:]]

def _is_aru_verb(word: str) -> bool:
    return any(aru_ending for aru_ending in _aru_verbs if word.endswith(aru_ending))

def get_word_stems(word: str, is_ichidan_verb: bool = False, is_godan: bool = False) -> list[str]:
    try:
        if _is_aru_verb(word):
            return [word[:-2] + end for end in _aru_mappings[word[-2:]]]
        if is_ichidan_verb:
            return [word[:-1] + end for end in _ichidan_endings]
        if is_godan:
            return [word[:-1] + end for end in _1_character_mappings[word[-1]]]
        if word[-2:] in _2_character_mappings:
            return [word[:-2] + end for end in _2_character_mappings[word[-2:]]]
        if word[-1] in _1_character_mappings:
            if word[-1] == "る":
                return [word[:-1] + end for end in _godan_ru_or_ichidan_endings]
            return [word[:-1] + end for end in _1_character_mappings[word[-1]]]
    except KeyError:
        mylog.warning(f"get_word_stems failed to handle {word}, returning empty list ")
    return [word]

def _get_stem(word: str, stem_index: int, is_ichidan_verb: bool = False, is_godan: bool = False) -> str:
    try:
        if _is_aru_verb(word):
            return word[:-2] + _aru_mappings[word[-2:]][stem_index]
        if is_ichidan_verb:
            return word[:-1]
        if is_godan:
            return word[:-1] + _1_character_mappings[word[-1]][stem_index]
        if word[-2:] == "ます":
            return word[:-2] + _masu_forms_by_index[stem_index]
        if word[-2:] in _2_character_mappings:
            return word[:-2] + _2_character_mappings[word[-2:]][stem_index]
        if word[-1] in _1_character_mappings:
            if word[-1] != "る":
                return word[:-1] + _1_character_mappings[word[-1]][stem_index]
            return word[:-1] + _1_character_mappings[word[-1]][stem_index]
    except KeyError:
        mylog.warning(f"_get_stem failed to handle {word}, returning empty list ")
    return word

def get_i_stem(word: str, is_ichidan: bool = False, is_godan: bool = False) -> str:
    return _get_stem(word, _i_stem_index, is_ichidan, is_godan)

def get_a_stem(word: str, is_ichidan: bool = False, is_godan: bool = False) -> str:
    return _get_stem(word, _a_stem_index, is_ichidan, is_godan)

def get_e_stem(word: str, is_ichidan: bool = False, is_godan: bool = False) -> str:
    return _get_stem(word, _e_stem_index, is_ichidan, is_godan)

def get_te_stem(word: str, is_ichidan: bool = False, is_godan: bool = False) -> str:
    return _get_stem(word, _te_stem_index, is_ichidan, is_godan)

def get_i_stem_vocab(vocab: VocabNote, form: str = "") -> str:
    return get_i_stem(form if form else vocab.get_question(), vocab.parts_of_speech.is_ichidan(), vocab.parts_of_speech.is_godan())

def get_e_stem_vocab(vocab: VocabNote, form: str = "") -> str:
    return get_e_stem(form if form else vocab.get_question(), vocab.parts_of_speech.is_ichidan(), vocab.parts_of_speech.is_godan())

def get_a_stem_vocab(vocab: VocabNote, form: str = "") -> str:
    return get_a_stem(form if form else vocab.get_question(), vocab.parts_of_speech.is_ichidan(), vocab.parts_of_speech.is_godan())

def get_te_stem_vocab(vocab: VocabNote, form: str = "") -> str:
    return get_te_stem(form if form else vocab.get_question(), vocab.parts_of_speech.is_ichidan(), vocab.parts_of_speech.is_godan())
