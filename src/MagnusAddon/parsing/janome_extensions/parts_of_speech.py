from sysutils import kana_utils
from sysutils.utils import StringUtils

class PartsOfSpeech:
    all_known = set[str]()
    def __init__(self, unparsed: str) -> None:
        PartsOfSpeech.all_known.add(unparsed)
        parts = StringUtils.extract_comma_separated_values(unparsed)
        self._parts = parts
        self.level1 = _japanese_to_part_of_speech[parts[0]]
        self.level2 = _japanese_to_part_of_speech[parts[1]]
        self.level3 = _japanese_to_part_of_speech[parts[2]]
        self.level4 = _japanese_to_part_of_speech[parts[3]]

    def is_noise(self) -> bool: return self.level1.japanese in ['記号']

    def translate(self) -> str:
        return ','.join([_part_of_speech_string_translation[pos] for pos in self._parts])

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


_full_parts_of_speech = [
    #other
    'その他,間投,*,*',
    'フィラー,*,*,*',

    #adverb
    '副詞,一般,*,*',
    '副詞,助詞類接続,*,*',

    '助動詞,*,*,*', #bound auxiliary/auxiliary verb

    #Particle
    '助詞,並立助詞,*,*',
    '助詞,係助詞,*,*',
    '助詞,副助詞,*,*',
    '助詞,副助詞／並立助詞／終助詞,*,*',
    '助詞,副詞化,*,*',
    '助詞,接続助詞,*,*',
    #Particle -> CaseMarking
    '助詞,格助詞,一般,*',
    '助詞,格助詞,引用,*',
    '助詞,格助詞,連語,*',

    '助詞,特殊,*,*',
    '助詞,終助詞,*,*',
    '助詞,連体化,*,*',

    #verb
    '動詞,接尾,*,*',
    '動詞,自立,*,*',
    '動詞,非自立,*,*',

    #noun
    '名詞,サ変接続,*,*',
    '名詞,ナイ形容詞語幹,*,*',
    '名詞,一般,*,*',
    #noun -> pronoun
    '名詞,代名詞,一般,*',
    '名詞,代名詞,縮約,*',
    '名詞,副詞可能,*,*',
    '名詞,動詞非自立的,*,*',

    #noun -> proper noun
    '名詞,固有名詞,一般,*',

    #noun -> proper noun -> person
    '名詞,固有名詞,人名,一般',
    '名詞,固有名詞,人名,名',
    '名詞,固有名詞,人名,姓',

    #noun -> proper noun -> location
    '名詞,固有名詞,地域,一般',
    '名詞,固有名詞,地域,国',

    '名詞,固有名詞,組織,*',


    '名詞,形容動詞語幹,*,*',#na_adjective_stem

    #suffix
    '名詞,接尾,サ変接続,*',
    '名詞,接尾,一般,*',
    '名詞,接尾,人名,*',
    '名詞,接尾,副詞可能,*',
    '名詞,接尾,助動詞語幹,*',
    '名詞,接尾,助数詞,*',
    '名詞,接尾,地域,*',
    '名詞,接尾,形容動詞語幹,*',
    '名詞,接尾,特殊,*',

    '名詞,数,*,*',#numeric
    '名詞,特殊,助動詞語幹,*', #special_auxiliary_verb_stem

    #NonSelfReliant
    '名詞,非自立,一般,*',
    '名詞,非自立,副詞可能,*',
    '名詞,非自立,助動詞語幹,*',
    '名詞,非自立,形容動詞語幹,*',

    #adjective
    '形容詞,接尾,*,*',
    '形容詞,自立,*,*',
    '形容詞,非自立,*,*',

    '感動詞,*,*,*',#interjection

    '接続詞,*,*,*',#conjunction

    #prefix
    '接頭詞,名詞接続,*,*',
    '接頭詞,形容詞接続,*,*',
    '接頭詞,数接続,*,*',

    #symbol
    '記号,アルファベット,*,*',
    '記号,一般,*,*',
    '記号,句点,*,*',
    '記号,括弧閉,*,*',
    '記号,括弧開,*,*',
    '記号,空白,*,*',
    '記号,読点,*,*',

    '連体詞,*,*,*']

class FullPartsOfSpeech:
    class Other:
        interjection = PartsOfSpeech('その他,間投,*,*')
        filler = PartsOfSpeech('フィラー,*,*,*')

    class Adverb:
        general = PartsOfSpeech('副詞,一般,*,*')
        particle_connection = PartsOfSpeech('副詞,助詞類接続,*,*')

    bound_auxiliary = PartsOfSpeech('助動詞,*,*,*')

    class Particle:
        coordinating_conjunction = PartsOfSpeech('助詞,並立助詞,*,*')
        binding = PartsOfSpeech('助詞,係助詞,*,*')
        adverbial = PartsOfSpeech('助詞,副助詞,*,*')
        adverbial_coordinating_ending = PartsOfSpeech('助詞,副助詞／並立助詞／終助詞,*,*')
        adverbialization = PartsOfSpeech('助詞,副詞化,*,*')
        conjunctive = PartsOfSpeech('助詞,接続助詞,*,*')
        class CaseMarking:
            general = PartsOfSpeech('助詞,格助詞,一般,*')
            quotation = PartsOfSpeech('助詞,格助詞,引用,*')
            compound = PartsOfSpeech('助詞,格助詞,連語,*')

        special = PartsOfSpeech('助詞,特殊,*,*')
        sentence_ending = PartsOfSpeech('助詞,終助詞,*,*')
        adnominalization = PartsOfSpeech('助詞,連体化,*,*')

    class Verb:
        suffix = PartsOfSpeech('動詞,接尾,*,*')
        independent = PartsOfSpeech('動詞,自立,*,*')
        non_independent = PartsOfSpeech('動詞,非自立,*,*')

    class Noun:
        suru_verb = PartsOfSpeech('名詞,サ変接続,*,*')
        negative_adjective_stem = PartsOfSpeech('名詞,ナイ形容詞語幹,*,*')
        general = PartsOfSpeech('名詞,一般,*,*')
        class Pronoun:
            general = PartsOfSpeech('名詞,代名詞,一般,*')
            contracted = PartsOfSpeech('名詞,代名詞,縮約,*')
        adv_possible = PartsOfSpeech('名詞,副詞可能,*,*')
        auxiliary_verb = PartsOfSpeech('名詞,動詞非自立的,*,*')

        class ProperNoun:
            general = PartsOfSpeech('名詞,固有名詞,一般,*')

            class Person:
                general = PartsOfSpeech('名詞,固有名詞,人名,一般')
                firstname = PartsOfSpeech('名詞,固有名詞,人名,名')
                surname = PartsOfSpeech('名詞,固有名詞,人名,姓')

            class Location:
                general = PartsOfSpeech('名詞,固有名詞,地域,一般')
                country = PartsOfSpeech('名詞,固有名詞,地域,国')

            organization = PartsOfSpeech('名詞,固有名詞,組織,*')

        na_adjective_stem = PartsOfSpeech('名詞,形容動詞語幹,*,*')

        class Suffix:
            suru_verb_connection = PartsOfSpeech('名詞,接尾,サ変接続,*')
            general = PartsOfSpeech('名詞,接尾,一般,*')
            persons_name = PartsOfSpeech('名詞,接尾,人名,*')
            adv_possible = PartsOfSpeech('名詞,接尾,副詞可能,*')
            auxiliary_verb_stem = PartsOfSpeech('名詞,接尾,助動詞語幹,*')
            counter = PartsOfSpeech('名詞,接尾,助数詞,*')
            region = PartsOfSpeech('名詞,接尾,地域,*')
            na_adjective_stem = PartsOfSpeech('名詞,接尾,形容動詞語幹,*')
            special = PartsOfSpeech('名詞,接尾,特殊,*')

        numeric = PartsOfSpeech('名詞,数,*,*')
        special_auxiliary_verb_stem = PartsOfSpeech('名詞,特殊,助動詞語幹,*')

        class NonSelfReliant:
            general = PartsOfSpeech('名詞,非自立,一般,*')
            adv_possible = PartsOfSpeech('名詞,非自立,副詞可能,*')
            auxiliary_verb_stem = PartsOfSpeech('名詞,非自立,助動詞語幹,*')
            na_adjective_stem = PartsOfSpeech('名詞,非自立,形容動詞語幹,*')

    class Adjective:
        suffix = PartsOfSpeech('形容詞,接尾,*,*')
        independent = PartsOfSpeech('形容詞,自立,*,*')
        non_independent = PartsOfSpeech('形容詞,非自立,*,*')

    interjection = PartsOfSpeech('感動詞,*,*,*')

    conjunction = PartsOfSpeech('接続詞,*,*,*')

    class Prefix:
        noun = PartsOfSpeech('接頭詞,名詞接続,*,*')
        adjective = PartsOfSpeech('接頭詞,形容詞接続,*,*')
        number = PartsOfSpeech('接頭詞,数接続,*,*')

    class Symbol:
        alphabet = PartsOfSpeech('記号,アルファベット,*,*')
        general = PartsOfSpeech('記号,一般,*,*')
        period = PartsOfSpeech('記号,句点,*,*')
        closing_bracket = PartsOfSpeech('記号,括弧閉,*,*')
        opening_bracket = PartsOfSpeech('記号,括弧開,*,*')
        space = PartsOfSpeech('記号,空白,*,*')
        comma = PartsOfSpeech('記号,読点,*,*')

    pre_noun_adjectival = PartsOfSpeech('連体詞,*,*,*')




