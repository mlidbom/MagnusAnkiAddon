from sysutils.utils import StringUtils

class PartsOfSpeech:
    def __init__(self, unparsed: str) -> None:
        parts = StringUtils.extract_comma_separated_values(unparsed)
        self._parts = parts
        self.level1japanese = parts[0]
        self.level2japanese = parts[1]
        self.level3japanese = parts[2]
        self.level4japanese = parts[3]
        self.level1 = _japanese_to_part_of_speech[parts[0]]
        self.level2 = _japanese_to_part_of_speech[parts[1]]
        self.level3 = _japanese_to_part_of_speech[parts[2]]
        self.level4 = _japanese_to_part_of_speech[parts[3]]

    def is_noise(self) -> bool: return self.level1japanese in ['記号']

    def translate(self) -> str:
        return ','.join([_part_of_speech_string_translation[pos] for pos in self._parts])

class PartOfSpeech:
    def __init__(self, japanese: str, english: str, explanation: str):
        self.japanese = japanese
        self.english = english
        self.explanation = explanation

    def __str__(self) -> str: return f"PartOfSpeech('{self.japanese}', '{self.english}')"

_level_1 = [
    PartOfSpeech('副詞', 'adverb', "Modifies verbs/adjectives"),
    PartOfSpeech('助詞', 'particle', "Functional word indicating relation"),
    PartOfSpeech('接続詞', 'conjunction', "Connects words/clauses"),
    PartOfSpeech('名詞', 'noun', "Names things or ideas"),
    PartOfSpeech('記号', 'symbol', "Punctuation, special symbols"),
    PartOfSpeech('感動詞', 'exclamation', "Expresses emotion"),
    PartOfSpeech('接頭詞', 'prefix', "Added to beginning of words"),
    PartOfSpeech('動詞', 'verb', "Indicates action"),
    PartOfSpeech('フィラー', 'filler', "Sound/word filling a pause"),
    PartOfSpeech('助動詞', 'auxiliary-verb', "Modifies verb tense/mood"),
    PartOfSpeech('その他', 'others', "Miscellaneous, doesn't fit other categories"),
    PartOfSpeech('連体詞', 'adnominal-adjective', "Modifies nouns directly"),
    PartOfSpeech('形容詞', 'adjective', "Describes nouns")
]

_level_2_3_4 = [
    PartOfSpeech('*', '*', "Wildcard or general category"),
    PartOfSpeech('一般', 'general', "Generic, non-specific")
]

_level_2_3 = [
    PartOfSpeech('サ変接続', 'suru-verb', "Nouns convertible into verbs with 'する'"),
    PartOfSpeech('特殊', 'special', "Irregular forms"),
    PartOfSpeech('副詞可能', 'adverbial', "Nouns/verbs that can function as adverbs"),
    PartOfSpeech('形容動詞語幹', 'adjectival-verb-stem', "Base form of na-adjectives")
]

_level_2 = _level_2_3_4 + _level_2_3 + [
    PartOfSpeech('自立', 'independent', "Can stand alone, not dependent on other words"),
    PartOfSpeech('代名詞', 'pronoun', "Replaces a noun, e.g., he, she, it"),
    PartOfSpeech('係助詞', 'binding', "Connects words/clauses, e.g., は, も"),
    PartOfSpeech('読点', 'comma', "Punctuation to separate elements"),
    PartOfSpeech('連体化', 'adnominalization', "Turns word into modifier for nouns"),
    PartOfSpeech('副助詞', 'adverbial', "Adverbial particle, modifies verbs"),
    PartOfSpeech('副助詞／並立助詞／終助詞', 'adverbial/coordinating-conjunction/ending', "Various particle types"),
    PartOfSpeech('形容詞接続', 'adjective-connection', "Connects adjectives"),
    PartOfSpeech('副詞化', 'adverbialization', "Turns word into adverb"),
    PartOfSpeech('間投', 'interjection', "Expresses emotion or marks a pause"),
    PartOfSpeech('非自立', 'dependent', "Depends on another word to convey meaning"),
    PartOfSpeech('括弧閉', 'closing-bracket', "Closing bracket punctuation"),
    PartOfSpeech('括弧開', 'opening-bracket', "Opening bracket punctuation"),
    PartOfSpeech('接尾', 'suffix', "Appended to end of words"),
    PartOfSpeech('接続助詞', 'conjunctive', "Connects clauses or sentences"),
    PartOfSpeech('助詞類接続', 'particle-connection', "Connects particles"),
    PartOfSpeech('数', 'numeric', "Numerical expressions"),
    PartOfSpeech('動詞非自立的', 'auxiliary-verb', "Auxiliary verb form"),
    PartOfSpeech('数接続', 'numeric-connection', "Numeric connectors"),
    PartOfSpeech('句点', 'period', "Ending punctuation mark"),
    PartOfSpeech('格助詞', 'case-particle', "Indicates grammatical case"),
    PartOfSpeech('アルファベット', 'alphabet', "Alphabetical characters"),
    PartOfSpeech('ナイ形容詞語幹', 'negative-adjective-stem', "Negative adjective stem form"),
    PartOfSpeech('空白', 'space', "Whitespace or blank space"),
    PartOfSpeech('名詞接続', 'noun-connection', "Noun connectors"),
    PartOfSpeech('終助詞', 'sentence-ending', "Ends the sentence"),
    PartOfSpeech('固有名詞', 'proper-noun', "Names of specific entities, like Tokyo"),
    PartOfSpeech('並立助詞', 'coordinating-conjunction', "Connects equal grammatical items, e.g., and, or")
]

_level_3 = _level_2_3_4 + _level_2_3 + [
    PartOfSpeech('助数詞', 'counter', "Counting words, e.g., つ, 本"),
    PartOfSpeech('連語', 'compound', "Compound words, two or more words combined"),
    PartOfSpeech('人名', 'person-name', "Names of people"),
    PartOfSpeech('地域', 'region', "Names of regions, cities, countries"),
    PartOfSpeech('引用', 'quotation', "Quotation or citation"),
    PartOfSpeech('組織', 'organization', "Names of organizations, companies"),
    PartOfSpeech('助動詞語幹', 'auxiliary-verb-stem', "Base form of auxiliary verbs"),
    PartOfSpeech('縮約', 'contraction', "Contracted forms, e.g., can't, don't")
]

_level_4 = _level_2_3_4 + [
    PartOfSpeech('名', 'first-name', "Given names"),
    PartOfSpeech('姓', 'surname', "Family names or surnames"),
    PartOfSpeech('国', 'country', "Names of countries")
]



_parts_of_speech = _level_1 + _level_2 + _level_3 + _level_4

_japanese_to_part_of_speech = {pos.japanese: pos for pos in _parts_of_speech}
_part_of_speech_string_translation = {pos.japanese: pos.english for pos in _parts_of_speech}
