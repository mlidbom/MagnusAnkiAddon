# noinspection PyUnusedClass, PyUnusedName
from __future__ import annotations

from typing import override

from autoslot import Slots
from jaslib.sysutils import kana_utils
from typed_linq_collections.collections.q_set import QSet


class JNPartsOfSpeech(Slots):
    @classmethod
    def fetch(cls, unparsed: str) -> JNPartsOfSpeech:
        return _full_parts_of_speech_dictionary[unparsed]

    def __init__(self, level1: str, level2: str = "*", level3: str = "*", level4: str = "*") -> None:
        self.level1: PartOfSpeechDescription = _japanese_to_part_of_speech[level1]
        self.level2: PartOfSpeechDescription = _japanese_to_part_of_speech[level2]
        self.level3: PartOfSpeechDescription = _japanese_to_part_of_speech[level3]
        self.level4: PartOfSpeechDescription = _japanese_to_part_of_speech[level4]

    def is_non_word_character(self) -> bool: return self.level1.japanese in ["記号"]

    def is_noun(self) -> bool: return self.level1.japanese in ["名詞"]

    @override
    def __repr__(self) -> str:
        return "".join([
                "1:" + kana_utils.pad_to_length(self.level1.japanese, 5),
                "2:" + kana_utils.pad_to_length(self.level2.japanese.replace("*", ""), 6),
                "3:" + kana_utils.pad_to_length(self.level3.japanese.replace("*", ""), 6),
                "4:" + kana_utils.pad_to_length(self.level4.japanese.replace("*", ""), 6)])

class PartOfSpeechDescription(Slots):
    def __init__(self, japanese: str, english: str, explanation: str) -> None:
        self.japanese: str = japanese
        self.english: str = english
        self.explanation: str = explanation

    @override
    def __repr__(self) -> str: return self.english

_level_1 = [
        PartOfSpeechDescription("名詞", "noun", "Names things or ideas"),
        PartOfSpeechDescription("形容詞", "i-adjective", "Describes nouns"),
        PartOfSpeechDescription("連体詞", "pre-noun adjectival / adnominal-adjective", "Modifies nouns directly"),
        PartOfSpeechDescription("接続詞的", "conjunctive", "words or expressions that function in a manner similar to conjunctions"),
        PartOfSpeechDescription("動詞", "verb", "Indicates action"),
        PartOfSpeechDescription("副詞", "adverb", "Modifies verbs/adjectives"),
        PartOfSpeechDescription("助動詞", "bound-auxiliary", "Modifies verb tense/mood"),
        PartOfSpeechDescription("助詞", "particle", "Functional word indicating relation such as marking direct object, subject etc"),
        PartOfSpeechDescription("接続詞", "conjunction", "Connects words/clauses"),
        PartOfSpeechDescription("感動詞", "interjection", "Expresses emotion"),
        PartOfSpeechDescription("接頭詞", "prefix", "Added to beginning of words"),
        PartOfSpeechDescription("フィラー", "filler", "Sound/word filling a pause"),
        PartOfSpeechDescription("記号", "symbol", "Punctuation, special symbols"),
        PartOfSpeechDescription("その他", "others", "Miscellaneous, doesn't fit other categories")
]

_level_2_3_4 = [
        PartOfSpeechDescription("*", "*", "Wildcard or general category"),
        PartOfSpeechDescription("一般", "general", "Generic, non-specific")
]

_level_2_3 = [
        PartOfSpeechDescription("サ変接続", "suru-verb", "Nouns convertible into verbs with 'する'"),
        PartOfSpeechDescription("特殊", "special", "Irregular forms"),
        PartOfSpeechDescription("副詞可能", "adverbial", "Nouns/verbs that can function as adverbs"),
        PartOfSpeechDescription("形容動詞語幹", "na-adjective stem", "Base form of na-adjectives")
]

_level_2 = _level_2_3_4 + _level_2_3 + [
        PartOfSpeechDescription("自立", "independent", "Not dependent on other words"),
        PartOfSpeechDescription("動詞接続", "verb-connective", "indicates a form or a word that is used to connect with or modify a verb"),
        PartOfSpeechDescription("代名詞", "pronoun", "Replaces a noun, e.g., he, she, it"),
        PartOfSpeechDescription("係助詞", "binding", "Connects words/clauses, e.g., は, も"),
        PartOfSpeechDescription("読点", "comma", "Punctuation to separate elements"),
        PartOfSpeechDescription("連体化", "adnominalization", "Turns word into modifier for nouns"),
        PartOfSpeechDescription("副助詞", "adverbial", "Adverbial particle, modifies verbs"),
        PartOfSpeechDescription("副助詞／並立助詞／終助詞", "adverbial/coordinating-conjunction/ending", "Various particle types"),
        PartOfSpeechDescription("形容詞接続", "adjective-connection", "Connects adjectives"),
        PartOfSpeechDescription("副詞化", "adverbialization", "Turns word into adverb"),
        PartOfSpeechDescription("間投", "interjection", "Expresses emotion or marks a pause"),
        PartOfSpeechDescription("非自立", "dependent", "Depends on another word to convey meaning"),
        PartOfSpeechDescription("括弧閉", "closing-bracket", "Closing bracket punctuation"),
        PartOfSpeechDescription("括弧開", "opening-bracket", "Opening bracket punctuation"),
        PartOfSpeechDescription("接尾", "suffix", "Appended to end of words"),
        PartOfSpeechDescription("接続助詞", "conjunctive", "Connects clauses or sentences"),
        PartOfSpeechDescription("助詞類接続", "particle-connection", "Connects particles"),
        PartOfSpeechDescription("数", "numeric", "Numerical expressions"),
        PartOfSpeechDescription("動詞非自立的", "auxiliary-verb", "Auxiliary verb form"),
        PartOfSpeechDescription("数接続", "numeric-connection", "Numeric connectors"),
        PartOfSpeechDescription("句点", "period", "Ending punctuation mark"),
        PartOfSpeechDescription("格助詞", "case-particle", "Indicates grammatical case"),
        PartOfSpeechDescription("アルファベット", "alphabet", "Alphabetical characters"),
        PartOfSpeechDescription("ナイ形容詞語幹", "negative-adjective-stem", "Negative adjective stem form"),
        PartOfSpeechDescription("空白", "space", "Whitespace or blank space"),
        PartOfSpeechDescription("名詞接続", "noun-connection", "Noun connectors"),
        PartOfSpeechDescription("終助詞", "sentence-ending", "Ends the sentence"),
        PartOfSpeechDescription("固有名詞", "proper-noun", "Names of specific entities, like Tokyo"),
        PartOfSpeechDescription("並立助詞", "coordinating-conjunction", "Connects equal grammatical items, e.g., and, or"),
        PartOfSpeechDescription("引用文字列", "quoted-character-string", "quoted-character-string")
]

_level_3 = _level_2_3_4 + _level_2_3 + [
        PartOfSpeechDescription("助数詞", "counter", "Counting words, e.g., つ, 本"),
        PartOfSpeechDescription("連語", "compound", "Compound words, two or more words combined"),
        PartOfSpeechDescription("人名", "person-name", "Names of people"),
        PartOfSpeechDescription("地域", "region", "Names of regions, cities, countries"),
        PartOfSpeechDescription("引用", "quotation", "Quotation or citation"),
        PartOfSpeechDescription("組織", "organization", "Names of organizations, companies"),
        PartOfSpeechDescription("助動詞語幹", "auxiliary-verb-stem", "Base form of auxiliary verbs"),
        PartOfSpeechDescription("縮約", "contraction", "Contracted forms, e.g., can't, don't")
]

_level_4 = _level_2_3_4 + [
        PartOfSpeechDescription("名", "first-name", "Given names"),
        PartOfSpeechDescription("姓", "surname", "Family names or surnames"),
        PartOfSpeechDescription("国", "country", "Names of countries")
]
_all_parts_of_speech = _level_1 + _level_2 + _level_3 + _level_4

_japanese_to_part_of_speech: dict[str, PartOfSpeechDescription] = {pos.japanese: pos for pos in _all_parts_of_speech}
_full_parts_of_speech_dictionary = dict[str, JNPartsOfSpeech]()

def _add_full_part_of_speech(level1: str, level2: str = "*", level3: str = "*", level4: str = "*") -> JNPartsOfSpeech:
    combined = f"{level1},{level2},{level3},{level4}"
    parts_of_speech = JNPartsOfSpeech(level1, level2, level3, level4)
    _full_parts_of_speech_dictionary[combined] = parts_of_speech
    return parts_of_speech

# noinspection PyUnusedClass, PyUnusedName
class JNPOS(Slots):
    filler: JNPartsOfSpeech = _add_full_part_of_speech("フィラー")
    bound_auxiliary: JNPartsOfSpeech = _add_full_part_of_speech("助動詞")  # た, ない, だ
    pre_noun_adjectival: JNPartsOfSpeech = _add_full_part_of_speech("連体詞")  # こんな
    interjection: JNPartsOfSpeech = _add_full_part_of_speech("感動詞")
    conjunction: JNPartsOfSpeech = _add_full_part_of_speech("接続詞")

    # noinspection PyUnusedClass, PyUnusedName
    class Other(Slots):
        interjection: JNPartsOfSpeech = _add_full_part_of_speech("その他", "間投")

    class Adverb(Slots):
        general: JNPartsOfSpeech = _add_full_part_of_speech("副詞", "一般")  # もう, そんなに
        particle_connection: JNPartsOfSpeech = _add_full_part_of_speech("副詞", "助詞類接続")  # こんなに

    # noinspection PyUnusedClass, PyUnusedName
    class Particle(Slots):
        coordinating_conjunction: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "並立助詞")  # たり
        binding: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "係助詞")  # は, も
        adverbial: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "副助詞")  # まで
        adverbial_coordinating_ending: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "副助詞／並立助詞／終助詞")
        adverbialization: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "副詞化")  # に
        conjunctive: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "接続助詞")  # て, と, し
        special: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "特殊")
        sentence_ending: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "終助詞")  # な
        adnominalization: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "連体化")  # の

        # noinspection PyUnusedClass, PyUnusedName
        class CaseMarking(Slots):
            general: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "格助詞", "一般")  # が, に
            quotation: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "格助詞", "引用")
            compound: JNPartsOfSpeech = _add_full_part_of_speech("助詞", "格助詞", "連語")

    class Verb(Slots):
        suffix: JNPartsOfSpeech = _add_full_part_of_speech("動詞", "接尾")  # れる passive
        independent: JNPartsOfSpeech = _add_full_part_of_speech("動詞", "自立")  # 疲れる, する, 走る
        dependent: JNPartsOfSpeech = _add_full_part_of_speech("動詞", "非自立")  # いる progressive/perfect, いく

        all_types: QSet[JNPartsOfSpeech] = QSet((independent, dependent, suffix))

    # noinspection PyUnusedClass, PyUnusedName
    class Noun(Slots):
        suru_verb: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "サ変接続")  # 話
        negative_adjective_stem: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "ナイ形容詞語幹")
        general: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "一般")  # 自分
        adverbial: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "副詞可能")  # 今
        auxiliary_verb: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "動詞非自立的")
        na_adjective_stem: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "形容動詞語幹")  # 好き
        numeric: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "数")
        conjunctive: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "接続詞的")
        quoted_character_string: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "引用文字列")  # ???

        # noinspection PyUnusedClass, PyUnusedName
        class Pronoun(Slots):
            general: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "代名詞", "一般")  # あいつ
            contracted: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "代名詞", "縮約")

        # noinspection PyUnusedClass, PyUnusedName
        class ProperNoun(Slots):
            general: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "固有名詞", "一般")
            organization: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "固有名詞", "組織")

            # noinspection PyUnusedClass, PyUnusedName
            class Person(Slots):
                general: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "固有名詞", "人名", "一般")
                firstname: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "固有名詞", "人名", "名")
                surname: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "固有名詞", "人名", "姓")

            # noinspection PyUnusedClass, PyUnusedName
            class Location(Slots):
                general: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "固有名詞", "地域", "一般")
                country: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "固有名詞", "地域", "国")

        # noinspection PyUnusedClass, PyUnusedName
        class Suffix(Slots):
            suru_verb_connection: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "接尾", "サ変接続")
            general: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "接尾", "一般")
            persons_name: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "接尾", "人名")
            adverbial: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "接尾", "副詞可能")
            auxiliary_verb_stem: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "接尾", "助動詞語幹")
            counter: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "接尾", "助数詞")
            region: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "接尾", "地域")
            na_adjective_stem: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "接尾", "形容動詞語幹")
            special: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "接尾", "特殊")

        # noinspection PyUnusedClass, PyUnusedName
        class Special(Slots):
            auxiliary_verb_stem: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "特殊", "助動詞語幹")

        # noinspection PyUnusedClass, PyUnusedName
        class Dependent(Slots):
            general: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "非自立", "一般")  # こと
            adverbial: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "非自立", "副詞可能")  # なか
            auxiliary_verb_stem: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "非自立", "助動詞語幹")
            na_adjective_stem: JNPartsOfSpeech = _add_full_part_of_speech("名詞", "非自立", "形容動詞語幹")

    # noinspection PyUnusedClass, PyUnusedName
    class Adjective(Slots):
        suffix: JNPartsOfSpeech = _add_full_part_of_speech("形容詞", "接尾")
        independent: JNPartsOfSpeech = _add_full_part_of_speech("形容詞", "自立")
        dependent: JNPartsOfSpeech = _add_full_part_of_speech("形容詞", "非自立")  # よかった
        all_types: QSet[JNPartsOfSpeech] = QSet((independent, dependent, suffix))

    # noinspection PyUnusedClass, PyUnusedName
    class Prefix(Slots):
        noun: JNPartsOfSpeech = _add_full_part_of_speech("接頭詞", "名詞接続")
        adjective: JNPartsOfSpeech = _add_full_part_of_speech("接頭詞", "形容詞接続")
        number: JNPartsOfSpeech = _add_full_part_of_speech("接頭詞", "数接続")
        verb_connective: JNPartsOfSpeech = _add_full_part_of_speech("接頭詞", "動詞接続")

    # noinspection PyUnusedClass, PyUnusedName
    class Symbol(Slots):
        alphabet: JNPartsOfSpeech = _add_full_part_of_speech("記号", "アルファベット")
        general: JNPartsOfSpeech = _add_full_part_of_speech("記号", "一般")
        period: JNPartsOfSpeech = _add_full_part_of_speech("記号", "句点")
        closing_bracket: JNPartsOfSpeech = _add_full_part_of_speech("記号", "括弧閉")
        opening_bracket: JNPartsOfSpeech = _add_full_part_of_speech("記号", "括弧開")
        space: JNPartsOfSpeech = _add_full_part_of_speech("記号", "空白")
        comma: JNPartsOfSpeech = _add_full_part_of_speech("記号", "読点")
