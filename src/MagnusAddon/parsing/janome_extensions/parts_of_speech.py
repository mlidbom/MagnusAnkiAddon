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
    PartOfSpeech('副詞', 'adverb'),
    PartOfSpeech('助詞', 'particle'),
    PartOfSpeech('接続詞', 'conjunction'),
    PartOfSpeech('名詞', 'noun'),
    PartOfSpeech('記号', 'symbol'),
    PartOfSpeech('感動詞', 'exclamation'),
    PartOfSpeech('接頭詞', 'prefix'),
    PartOfSpeech('動詞', 'verb'),
    PartOfSpeech('フィラー', 'filler'),
    PartOfSpeech('助動詞', 'auxiliary-verb'),
    PartOfSpeech('その他', 'others'),
    PartOfSpeech('連体詞', 'adnominal-adjective'),
    PartOfSpeech('形容詞', 'adjective')]

_level_2_3_4 = [
    PartOfSpeech('*', '*'),
    PartOfSpeech('一般', 'general')]

_level_2_3 = [
    PartOfSpeech('サ変接続', 'suru-verb'),
    PartOfSpeech('特殊', 'special', "irregular verbs, special pronouns, etc that don't neatly fit into standard grammatical categories"),
    PartOfSpeech('副詞可能', 'adverbial'),
    PartOfSpeech('形容動詞語幹', 'adjectival-verb-stem')]

_level_2 = _level_2_3_4 + _level_2_3 + [
    PartOfSpeech('自立', 'independent'),
    PartOfSpeech('代名詞', 'pronoun'),
    PartOfSpeech('係助詞', 'binding'),
    PartOfSpeech('読点', 'comma'),
    PartOfSpeech('連体化', 'adnominalization'),
    PartOfSpeech('副助詞', 'adverbial'),
    PartOfSpeech('副助詞／並立助詞／終助詞', 'adverbial/coordinating-conjunction/ending'),
    PartOfSpeech('形容詞接続', 'adjective-connection'),
    PartOfSpeech('副詞化', 'adverbialization'),
    PartOfSpeech('間投', 'interjection'),
    PartOfSpeech('非自立', 'dependent'),
    PartOfSpeech('括弧閉', 'closing-bracket'),
    PartOfSpeech('括弧開', 'opening-bracket'),
    PartOfSpeech('接尾', 'suffix'),
    PartOfSpeech('接続助詞', 'conjunctive'),
    PartOfSpeech('助詞類接続', 'particle-connection'),
    PartOfSpeech('数', 'numeric'),
    PartOfSpeech('動詞非自立的', 'auxiliary-verb'),
    PartOfSpeech('数接続', 'numeric-connection'),
    PartOfSpeech('句点', 'period'),
    PartOfSpeech('格助詞', 'case-particle'),
    PartOfSpeech('アルファベット', 'alphabet'),
    PartOfSpeech('ナイ形容詞語幹', 'negative-adjective-stem'),
    PartOfSpeech('空白', 'space'),
    PartOfSpeech('名詞接続', 'noun-connection'),
    PartOfSpeech('終助詞', 'sentence-ending'),
    PartOfSpeech('固有名詞', 'proper-noun'),
    PartOfSpeech('並立助詞', 'coordinating-conjunction')]

_level_3 = _level_2_3_4 + _level_2_3 + [
    PartOfSpeech('助数詞', 'counter'),
    PartOfSpeech('連語', 'compound'),
    PartOfSpeech('人名', 'person-name'),
    PartOfSpeech('地域', 'region'),
    PartOfSpeech('引用', 'quotation'),
    PartOfSpeech('組織', 'organization'),
    PartOfSpeech('助動詞語幹', 'auxiliary-verb-stem'),
    PartOfSpeech('縮約', 'contraction')]

_level_4 = _level_2_3_4 + [
    PartOfSpeech('名', 'first-name'),
    PartOfSpeech('姓', 'surname'),
    PartOfSpeech('国', 'country')]



_parts_of_speech = _level_1 + _level_2 + _level_3 + _level_4

_japanese_to_part_of_speech = {pos.japanese: pos for pos in _parts_of_speech}
_part_of_speech_string_translation = {pos.japanese: pos.english for pos in _parts_of_speech}
