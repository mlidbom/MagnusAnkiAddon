"""xpos is the extended part of speech tag used for language specific information."""

#Japanese POS Tags: https://gist.github.com/masayu-a/e3eee0637c07d4019ec9
#Universal POS Tags: https://universaldependencies.org/u/pos/index.html
#Universal Dependency Relations https://universaldependencies.org/u/dep/index.html
from typing import Any

class UdJapanesePartOfSpeechTag:
    def __init__(self, japanese: str, english_tag:str, english_description: str) -> None:
        self.japanese = japanese
        self.english_tag = english_tag
        self.description = english_description

    def __str__(self) -> str: return self.description

    def __eq__(self, other:Any) -> bool:
        return (isinstance(other, UdJapanesePartOfSpeechTag)
                and other.japanese == self.japanese)

    def __hash__(self) -> int: return hash(self.japanese)


_english_pos_tag_dictionary: dict[str, UdJapanesePartOfSpeechTag] = dict()
_japanese_pos_tag_dictionary: dict[str, UdJapanesePartOfSpeechTag] = dict()

def get_tag(japanese:str) -> UdJapanesePartOfSpeechTag:
    return _japanese_pos_tag_dictionary[japanese]


def _add_tag(japanese: str, english_tag:str, english_description: str) -> UdJapanesePartOfSpeechTag:
    tag = UdJapanesePartOfSpeechTag(japanese, english_tag, english_description)
    _english_pos_tag_dictionary[english_description] = tag
    _japanese_pos_tag_dictionary[japanese] = tag
    return tag

adverb = _add_tag("副詞", "Adv", "adverb")

inflecting_dependent_word = _add_tag("助動詞", "Aux", "inflecting_dependent_word") #modified. Was: auxiliary_verb

particle_binding = _add_tag("助詞-係助詞", "P.bind", "particle_binding")
particle_adverbial = _add_tag("助詞-副助詞", "P.adv", "particle_adverbial")
particle_conjunctive = _add_tag("助詞-接続助詞", "P.conj", "particle_conjunctive")
particle_case = _add_tag("助詞-格助詞", "P.case", "particle_case")
particle_nominal = _add_tag("助詞-準体助詞", "P.nom", "particle_nominal")
particle_phrase_ending = _add_tag("助詞-終助詞", "P.fin", "particle_phrase_final")

verb_general = _add_tag("動詞-一般", "V.g", "verb_general")
verb_bound = _add_tag("動詞-非自立可能", "V.bnd", "verb_bound")

noun_common_verbal_suru = _add_tag("名詞-普通名詞-サ変可能", "N.c.vs", "noun_common_verbal_suru")
noun_common_verbal_adjectival = _add_tag("名詞-普通名詞-サ変形状詞可能", "N.c.vs.ana", "noun_common_verbal_adjectival")
noun_common_general = _add_tag("名詞-普通名詞-一般", "N.c.g", "noun_common_general")
noun_common_adverbial = _add_tag("名詞-普通名詞-副詞可能", "N.c.adv", "noun_common_adverbial")
noun_common_counter = _add_tag("名詞-普通名詞-助数詞可能", "N.c.count", "noun_common_counter")
noun_common_adjectival = _add_tag("名詞-普通名詞-形状詞可能", "N.c.ana", "noun_common_adjectival")

noun_auxiliary = _add_tag("名詞-助動詞語幹", "N.aux", "noun_auxiliary")
noun_pronoun = _add_tag("代名詞", "Pron", "noun_pronoun")

noun_proper_general = _add_tag("名詞-固有名詞-一般", "N.prop.g", "noun_proper_general")
noun_proper_name_general = _add_tag("名詞-固有名詞-人名-一般", "N.prop.n.g", "noun_proper_name_general")
noun_proper_name_firstname = _add_tag("名詞-固有名詞-人名-名", "N.prop.n.f", "noun_proper_name_firstname")
noun_proper_name_surname = _add_tag("名詞-固有名詞-人名-姓", "N.prop.n.s", "noun_proper_name_surname")
noun_proper_place_general = _add_tag("名詞-固有名詞-地名-一般", "N.prop.p.g", "noun_proper_place_general")
noun_proper_place_country = _add_tag("名詞-固有名詞-地名-国", "N.prop.p.c", "noun_proper_place_country")
noun_numeral = _add_tag("名詞-数詞", "N.num", "noun_numeral")

adjective_i_general = _add_tag("形容詞-一般", "Ai.g", "adjective_i_general")
adjective_i_bound = _add_tag("形容詞-非自立可能", "Ai.bnd", "adjective_i_bound")
adjectival_noun_tari = _add_tag("形状詞-タリ", "Ana.tari", "adjectival_noun_tari")
adjectival_noun_general = _add_tag("形状詞-一般", "Ana.g", "adjectival_noun_general")
adjectival_noun_auxiliary = _add_tag("形状詞-助動詞語幹", "Ana.aux", "adjectival_noun_auxiliary")

interjection_filler = _add_tag("感動詞-フィラー", "Interj.fill", "interjection_filler")
interjection_general = _add_tag("感動詞-一般", "Interj.g", "interjection_general")

suffix_verbal = _add_tag("接尾辞-動詞的", "Suff.v", "suffix_verbal")
suffix_nominal_verbal_suru = _add_tag("接尾辞-名詞的-サ変可能", "Suff.n.vs", "suffix_nominal_verbal_suru")
suffix_nominal_general = _add_tag("接尾辞-名詞的-一般", "Suff.n.g", "suffix_nominal_general")
suffix_nominal_adverbial = _add_tag("接尾辞-名詞的-副詞可能", "Suff.n.adv", "suffix_nominal_adverbial")
suffix_nominal_counter = _add_tag("接尾辞-名詞的-助数詞", "Suff.n.count", "suffix_nominal_counter")
suffix_adjective_i = _add_tag("接尾辞-形容詞的", "Suff.ai", "suffix_adjective_i")
suffix_adjectival_noun = _add_tag("接尾辞-形状詞的", "Suff.ana", "suffix_adjectival_noun")

conjunction = _add_tag("接続詞", "Conj", "conjunction")

prefix = _add_tag("接頭辞", "Pref", "prefix")

whitespace = _add_tag("空白", "Ws", "whitespace")

symbol_general = _add_tag("記号-一般", "Sym.g", "symbol_general")
symbol_character = _add_tag("記号-文字", "Sym.ch", "symbol_character")

supplementary_symbol_ascii_art_general = _add_tag("補助記号-ＡＡ-一般", "Supsym.aa.g", "supplementary_symbol_ascii_art_general")
supplementary_symbol_ascii_art_emoticon = _add_tag("補助記号-ＡＡ-顔文字", "Supsym.aa.e", "supplementary_symbol_ascii_art_emoticon")
supplementary_symbol_general = _add_tag("補助記号-一般", "Supsym.g", "supplementary_symbol_general")
supplementary_symbol_period = _add_tag("補助記号-句点", "Supsym.p", "supplementary_symbol_period")
supplementary_symbol_bracketopen = _add_tag("補助記号-括弧閉", "Supsym.bo", "supplementary_symbol_bracketopen")
supplementary_symbol_bracketclose = _add_tag("補助記号-括弧開", "Supsym.bc", "supplementary_symbol_bracketclose")
supplementary_symbol_comma = _add_tag("補助記号-読点", "Supsym.c", "supplementary_symbol_comma")

adnominal = _add_tag("連体詞", "Adn", "adnominal")
katakana = _add_tag("カタカナ文", "Katakana", "katakana")
chinese_writing = _add_tag("漢文", "Kanbun", "chinese_writing")

hesitation = _add_tag("言いよどみ", "Hesitation", "hesitation")

errors_omissions = _add_tag("web誤脱", "ErrorOmit", "errors_omissions")

dialect = _add_tag("方言", "Dialect", "dialect")

latin_alphabet = _add_tag("ローマ字文", "Lat", "latin_alphabet")

unknown_words = _add_tag("未知語", "Unknown", "unknown_words")
new_unknown_words = _add_tag("新規未知語", "NewUnknown", "new_unknown_words")