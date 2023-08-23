from sysutils import kana_utils
from sysutils.utils import StringUtils

class PartsOfSpeech:
    @staticmethod
    def fetch(unparsed: str) -> 'PartsOfSpeech':
        return _full_parts_of_speech_dictionary[unparsed]

    def __init__(self, level1:str, level2:str = "*", level3:str = "*", level4:str = "*") -> None:
        self.level1 = _japanese_to_part_of_speech[level1]
        self.level2 = _japanese_to_part_of_speech[level2]
        self.level3 = _japanese_to_part_of_speech[level3]
        self.level4 = _japanese_to_part_of_speech[level4]

    def is_noise(self) -> bool: return self.level1.japanese in ['記号']

    def translate(self) -> str:
        return ','.join([self.level1.english, self.level2.english, self.level3.english, self.level4.english])

    def __repr__(self) -> str:
        return "".join([
            "1:" + kana_utils.pad_to_length(self.level1.japanese, 5),
            "2:" + kana_utils.pad_to_length(self.level2.japanese.replace("*", ""), 6),
            "3:" + kana_utils.pad_to_length(self.level3.japanese.replace("*", ""), 6),
            "4:" + kana_utils.pad_to_length(self.level4.japanese.replace("*", ""), 6)])

    def is_verb(self) -> bool: return "verb" == self.level1.english


class PartOfSpeechDescription:
    def __init__(self, japanese: str, english: str, explanation: str):
        self.japanese = japanese
        self.english = english
        self.explanation = explanation

    def __repr__(self) -> str: return self.english

_level_1 = [
    PartOfSpeechDescription('名詞', 'noun', "Names things or ideas"),
    PartOfSpeechDescription('形容詞', 'i-adjective', "Describes nouns"),
    PartOfSpeechDescription('連体詞', 'pre-noun adjectival / adnominal-adjective', "Modifies nouns directly"),
    PartOfSpeechDescription('接続詞的', 'conjunctive', 'words or expressions that function in a manner similar to conjunctions'),
    PartOfSpeechDescription('動詞', 'verb', "Indicates action"),
    PartOfSpeechDescription('副詞', 'adverb', "Modifies verbs/adjectives"),
    PartOfSpeechDescription('助動詞', 'bound-auxiliary', "Modifies verb tense/mood"),
    PartOfSpeechDescription('助詞', 'particle', "Functional word indicating relation such as marking direct object, subject etc"),
    PartOfSpeechDescription('接続詞', 'conjunction', "Connects words/clauses"),
    PartOfSpeechDescription('感動詞', 'interjection', "Expresses emotion"),
    PartOfSpeechDescription('接頭詞', 'prefix', "Added to beginning of words"),
    PartOfSpeechDescription('フィラー', 'filler', "Sound/word filling a pause"),
    PartOfSpeechDescription('記号', 'symbol', "Punctuation, special symbols"),
    PartOfSpeechDescription('その他', 'others', "Miscellaneous, doesn't fit other categories")
]

_level_2_3_4 = [
    PartOfSpeechDescription('*', '*', "Wildcard or general category"),
    PartOfSpeechDescription('一般', 'general', "Generic, non-specific")
]

_level_2_3 = [
    PartOfSpeechDescription('サ変接続', 'suru-verb', "Nouns convertible into verbs with 'する'"),
    PartOfSpeechDescription('特殊', 'special', "Irregular forms"),
    PartOfSpeechDescription('副詞可能', 'adverbial', "Nouns/verbs that can function as adverbs"),
    PartOfSpeechDescription('形容動詞語幹', 'na-adjective stem', "Base form of na-adjectives")
]

_level_2 = _level_2_3_4 + _level_2_3 + [
    PartOfSpeechDescription('自立', 'independent', "Not dependent on other words"),
    PartOfSpeechDescription('動詞接続', 'verb-connective', "indicates a form or a word that is used to connect with or modify a verb"),
    PartOfSpeechDescription('代名詞', 'pronoun', "Replaces a noun, e.g., he, she, it"),
    PartOfSpeechDescription('係助詞', 'binding', "Connects words/clauses, e.g., は, も"),
    PartOfSpeechDescription('読点', 'comma', "Punctuation to separate elements"),
    PartOfSpeechDescription('連体化', 'adnominalization', "Turns word into modifier for nouns"),
    PartOfSpeechDescription('副助詞', 'adverbial', "Adverbial particle, modifies verbs"),
    PartOfSpeechDescription('副助詞／並立助詞／終助詞', 'adverbial/coordinating-conjunction/ending', "Various particle types"),
    PartOfSpeechDescription('形容詞接続', 'adjective-connection', "Connects adjectives"),
    PartOfSpeechDescription('副詞化', 'adverbialization', "Turns word into adverb"),
    PartOfSpeechDescription('間投', 'interjection', "Expresses emotion or marks a pause"),
    PartOfSpeechDescription('非自立', 'dependent', "Depends on another word to convey meaning"),
    PartOfSpeechDescription('括弧閉', 'closing-bracket', "Closing bracket punctuation"),
    PartOfSpeechDescription('括弧開', 'opening-bracket', "Opening bracket punctuation"),
    PartOfSpeechDescription('接尾', 'suffix', "Appended to end of words"),
    PartOfSpeechDescription('接続助詞', 'conjunctive', "Connects clauses or sentences"),
    PartOfSpeechDescription('助詞類接続', 'particle-connection', "Connects particles"),
    PartOfSpeechDescription('数', 'numeric', "Numerical expressions"),
    PartOfSpeechDescription('動詞非自立的', 'auxiliary-verb', "Auxiliary verb form"),
    PartOfSpeechDescription('数接続', 'numeric-connection', "Numeric connectors"),
    PartOfSpeechDescription('句点', 'period', "Ending punctuation mark"),
    PartOfSpeechDescription('格助詞', 'case-particle', "Indicates grammatical case"),
    PartOfSpeechDescription('アルファベット', 'alphabet', "Alphabetical characters"),
    PartOfSpeechDescription('ナイ形容詞語幹', 'negative-adjective-stem', "Negative adjective stem form"),
    PartOfSpeechDescription('空白', 'space', "Whitespace or blank space"),
    PartOfSpeechDescription('名詞接続', 'noun-connection', "Noun connectors"),
    PartOfSpeechDescription('終助詞', 'sentence-ending', "Ends the sentence"),
    PartOfSpeechDescription('固有名詞', 'proper-noun', "Names of specific entities, like Tokyo"),
    PartOfSpeechDescription('並立助詞', 'coordinating-conjunction', "Connects equal grammatical items, e.g., and, or")
]

_level_3 = _level_2_3_4 + _level_2_3 + [
    PartOfSpeechDescription('助数詞', 'counter', "Counting words, e.g., つ, 本"),
    PartOfSpeechDescription('連語', 'compound', "Compound words, two or more words combined"),
    PartOfSpeechDescription('人名', 'person-name', "Names of people"),
    PartOfSpeechDescription('地域', 'region', "Names of regions, cities, countries"),
    PartOfSpeechDescription('引用', 'quotation', "Quotation or citation"),
    PartOfSpeechDescription('組織', 'organization', "Names of organizations, companies"),
    PartOfSpeechDescription('助動詞語幹', 'auxiliary-verb-stem', "Base form of auxiliary verbs"),
    PartOfSpeechDescription('縮約', 'contraction', "Contracted forms, e.g., can't, don't")
]

_level_4 = _level_2_3_4 + [
    PartOfSpeechDescription('名', 'first-name', "Given names"),
    PartOfSpeechDescription('姓', 'surname', "Family names or surnames"),
    PartOfSpeechDescription('国', 'country', "Names of countries")
]
_all_parts_of_speech = _level_1 + _level_2 + _level_3 + _level_4

_japanese_to_part_of_speech: dict[str, PartOfSpeechDescription] = {pos.japanese: pos for pos in _all_parts_of_speech}
_part_of_speech_string_translation = {pos.japanese: pos.english for pos in _all_parts_of_speech}

_full_parts_of_speech_dictionary = dict[str, PartsOfSpeech]()

def _add_full_part_of_speech(level1:str, level2:str = "*", level3:str = "*", level4:str = "*") -> PartsOfSpeech:
    combined = f"{level1},{level2},{level3},{level4}"
    parts_of_speech = PartsOfSpeech(level1, level2, level3, level4)
    _full_parts_of_speech_dictionary[combined] = parts_of_speech
    return parts_of_speech

class PartsOfSpeechHierarchy:
    filler = _add_full_part_of_speech('フィラー')
    bound_auxiliary = _add_full_part_of_speech('助動詞')
    pre_noun_adjectival = _add_full_part_of_speech('連体詞')
    interjection = _add_full_part_of_speech('感動詞')
    conjunction = _add_full_part_of_speech('接続詞')

    class Other:
        interjection = _add_full_part_of_speech('その他', '間投')

    class Adverb:
        general = _add_full_part_of_speech('副詞', '一般')
        particle_connection = _add_full_part_of_speech('副詞', '助詞類接続')

    class Particle:
        coordinating_conjunction = _add_full_part_of_speech('助詞', '並立助詞')
        binding = _add_full_part_of_speech('助詞', '係助詞')
        adverbial = _add_full_part_of_speech('助詞', '副助詞')
        adverbial_coordinating_ending = _add_full_part_of_speech('助詞', '副助詞／並立助詞／終助詞')
        adverbialization = _add_full_part_of_speech('助詞', '副詞化')
        conjunctive = _add_full_part_of_speech('助詞', '接続助詞')
        special = _add_full_part_of_speech('助詞', '特殊')
        sentence_ending = _add_full_part_of_speech('助詞', '終助詞')
        adnominalization = _add_full_part_of_speech('助詞', '連体化')

        class CaseMarking:
            general = _add_full_part_of_speech('助詞', '格助詞', '一般')
            quotation = _add_full_part_of_speech('助詞', '格助詞', '引用')
            compound = _add_full_part_of_speech('助詞', '格助詞', '連語')

    class Verb:
        suffix = _add_full_part_of_speech('動詞', '接尾')
        independent = _add_full_part_of_speech('動詞', '自立')
        non_independent = _add_full_part_of_speech('動詞', '非自立')

    class Noun:
        suru_verb = _add_full_part_of_speech('名詞', 'サ変接続')
        negative_adjective_stem = _add_full_part_of_speech('名詞', 'ナイ形容詞語幹')
        general = _add_full_part_of_speech('名詞', '一般')
        adv_possible = _add_full_part_of_speech('名詞', '副詞可能')
        auxiliary_verb = _add_full_part_of_speech('名詞', '動詞非自立的')
        na_adjective_stem = _add_full_part_of_speech('名詞', '形容動詞語幹')
        numeric = _add_full_part_of_speech('名詞', '数')

        class Pronoun:
            general = _add_full_part_of_speech('名詞', '代名詞', '一般')
            contracted = _add_full_part_of_speech('名詞', '代名詞', '縮約')

        class ProperNoun:
            general = _add_full_part_of_speech('名詞', '固有名詞', '一般')
            organization = _add_full_part_of_speech('名詞', '固有名詞', '組織')

            class Person:
                general = _add_full_part_of_speech('名詞', '固有名詞', '人名', '一般')
                firstname = _add_full_part_of_speech('名詞', '固有名詞', '人名', '名')
                surname = _add_full_part_of_speech('名詞', '固有名詞', '人名', '姓')

            class Location:
                general = _add_full_part_of_speech('名詞', '固有名詞', '地域', '一般')
                country = _add_full_part_of_speech('名詞', '固有名詞', '地域', '国')

        class Suffix:
            suru_verb_connection = _add_full_part_of_speech('名詞', '接尾', 'サ変接続')
            general = _add_full_part_of_speech('名詞', '接尾', '一般')
            persons_name = _add_full_part_of_speech('名詞', '接尾', '人名')
            adv_possible = _add_full_part_of_speech('名詞', '接尾', '副詞可能')
            auxiliary_verb_stem = _add_full_part_of_speech('名詞', '接尾', '助動詞語幹')
            counter = _add_full_part_of_speech('名詞', '接尾', '助数詞')
            region = _add_full_part_of_speech('名詞', '接尾', '地域')
            na_adjective_stem = _add_full_part_of_speech('名詞', '接尾', '形容動詞語幹')
            special = _add_full_part_of_speech('名詞', '接尾', '特殊')

        class Special:
            auxiliary_verb_stem = _add_full_part_of_speech('名詞', '特殊', '助動詞語幹')

        class NonSelfReliant:
            general = _add_full_part_of_speech('名詞', '非自立', '一般')
            adv_possible = _add_full_part_of_speech('名詞', '非自立', '副詞可能')
            auxiliary_verb_stem = _add_full_part_of_speech('名詞', '非自立', '助動詞語幹')
            na_adjective_stem = _add_full_part_of_speech('名詞', '非自立', '形容動詞語幹')

    class Adjective:
        suffix = _add_full_part_of_speech('形容詞', '接尾')
        independent = _add_full_part_of_speech('形容詞', '自立')
        non_independent = _add_full_part_of_speech('形容詞', '非自立')

    class Prefix:
        noun = _add_full_part_of_speech('接頭詞', '名詞接続')
        adjective = _add_full_part_of_speech('接頭詞', '形容詞接続')
        number = _add_full_part_of_speech('接頭詞', '数接続')

    class Symbol:
        alphabet = _add_full_part_of_speech('記号', 'アルファベット')
        general = _add_full_part_of_speech('記号', '一般')
        period = _add_full_part_of_speech('記号', '句点')
        closing_bracket = _add_full_part_of_speech('記号', '括弧閉')
        opening_bracket = _add_full_part_of_speech('記号', '括弧開')
        space = _add_full_part_of_speech('記号', '空白')
        comma = _add_full_part_of_speech('記号', '読点')