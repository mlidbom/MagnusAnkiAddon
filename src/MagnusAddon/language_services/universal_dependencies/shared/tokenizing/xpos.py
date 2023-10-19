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

adverb = _add_tag("副詞", "Adv", "adverb") # adverbial_modifier{そう, もう, とりあえず, ちゃんと, なぜ, どう, ついに}, root{やっぱり, ぶらぶら}, adverbial_clause_modifier{ああ}

inflecting_dependent_word = _add_tag("助動詞", "Aux", "inflecting_dependent_word") # auxiliary{たら, なかっ, で, られ, てる, なく, たい, とい, に, れる, な, られる, ちゃう, ない, なら, て, せ, らしい, だ, た}, copula{じゃ, だっ, でし, に, だ}, fixed_multiword_expression{たら, だ, です}, root{だっ, だろう}, marker{ん}, coordinating_conjunction{だっ}

particle_binding = _add_tag("助詞-係助詞", "P.bind", "particle_binding") # case_marking{は, も}, fixed_multiword_expression{も}
particle_adverbial = _add_tag("助詞-副助詞", "P.adv", "particle_adverbial") # marker{って, たり, か, まで}, compound{ばっか}, case_marking{って, か, まで}
particle_conjunctive = _add_tag("助詞-接続助詞", "P.conj", "particle_conjunctive") # marker{し, ちゃ, ば, けど, と, て, から}

"""case_marking{じゃ, で, へ, が, の, に, と, から, を}, fixed_multiword_expression{が, に}, root{と}, unspecified_dependency{と}"""
particle_case_marking = _add_tag("助詞-格助詞", "P.case", "particle_case_marking") # case_marking{じゃ, で, へ, が, の, に, と, から, を}, fixed_multiword_expression{が, に}, root{と}, unspecified_dependency{と}
particle_nominal = _add_tag("助詞-準体助詞", "P.nom", "particle_nominal") # marker{の, ん}
particle_phrase_ending = _add_tag("助詞-終助詞", "P.fin", "particle_phrase_final") # marker{ね, な, じゃん, よ, か, ぞ}

verb_general = _add_tag("動詞-一般", "V.g", "verb_general") # root{食べ, 知ら, 入る, 食べよう, 会う, 気づか, 読ん, 当て, 助け, 逢え, 離れ, 逃げ, 思う, いう, 聞い, 探し, 言っ}, adverbial_clause_modifier{言え, 言わ, 聞か, 調べ, 出, 誘っ, 思っ, 言っ, 書く}, clausal_modifier_of_noun{持っ, 食べ, 捨てる, 知っ, 振り}
verb_bound = _add_tag("動詞-非自立可能", "V.bnd", "verb_bound") # oblique_nominal{いる}, fixed_multiword_expression{ある, し, いる, いく, おけ, もらえ, くれ}, root{行こう, なっ, あり, くる, やろう, あげる, 行っ, する, 見}, clausal_modifier_of_noun{する, 行き}, adverbial_clause_modifier{やっ, 得る, 忘れ, 来, なる, い}, auxiliary{する, し}, clausal_complement{ある}

noun_common_verbal_suru = _add_tag("名詞-普通名詞-サ変可能", "N.c.vs", "noun_common_verbal_suru")
noun_common_verbal_adjectival = _add_tag("名詞-普通名詞-サ変形状詞可能", "N.c.vs.ana", "noun_common_verbal_adjectival")
noun_common_general = _add_tag("名詞-普通名詞-一般", "N.c.g", "noun_common_general")

noun_common_adverbial = _add_tag("名詞-普通名詞-副詞可能", "N.c.adv", "noun_common_adverbial") # nominal_modifier{相変わらず, 前, 今}, oblique_nominal{一度, 所, 以外, 時, 夜, 中}, root{ため}, adverbial_modifier{朝, 全部, 普段, 絶対}
noun_common_counter = _add_tag("名詞-普通名詞-助数詞可能", "N.c.count", "noun_common_counter") # root{円}
noun_common_adjectival = _add_tag("名詞-普通名詞-形状詞可能", "N.c.ana", "noun_common_adjectival") # direct_object{楽}, adjectival_modifier{無表情}, root{ダメ}

noun_auxiliary = _add_tag("名詞-助動詞語幹", "N.aux", "noun_auxiliary")
noun_pronoun = _add_tag("代名詞", "Pron", "noun_pronoun") # oblique_nominal{何, 私, いつ, これ, そっち}, direct_object{私}, nominal_subject{あいつ, 俺}, root{何}, nominal_modifier{俺}

noun_proper_general = _add_tag("名詞-固有名詞-一般", "N.prop.g", "noun_proper_general")
noun_proper_name_general = _add_tag("名詞-固有名詞-人名-一般", "N.prop.n.g", "noun_proper_name_general")
noun_proper_name_firstname = _add_tag("名詞-固有名詞-人名-名", "N.prop.n.f", "noun_proper_name_firstname")
noun_proper_name_surname = _add_tag("名詞-固有名詞-人名-姓", "N.prop.n.s", "noun_proper_name_surname") # compound{藤宮}
noun_proper_place_general = _add_tag("名詞-固有名詞-地名-一般", "N.prop.p.g", "noun_proper_place_general") # compound{日代}
noun_proper_place_country = _add_tag("名詞-固有名詞-地名-国", "N.prop.p.c", "noun_proper_place_country")
noun_numeral = _add_tag("名詞-数詞", "N.num", "noun_numeral") # compound{二千九百}

adjective_i_general = _add_tag("形容詞-一般", "Ai.g", "adjective_i_general") # adverbial_clause_modifier{明るい}, clausal_modifier_of_noun{素晴らしい}, root{偉}
adjective_i_bound = _add_tag("形容詞-非自立可能", "Ai.bnd", "adjective_i_bound") # fixed_multiword_expression{ない, いい}, adverbial_clause_modifier{良く, いい}, root{よかっ, なかっ, 良かっ, いい, 良けれ, ない}, clausal_complement{よかっ}

adjectival_noun_tari = _add_tag("形状詞-タリ", "Ana.tari", "adjectival_noun_tari")
adjectival_noun_general = _add_tag("形状詞-一般", "Ana.g", "adjectival_noun_general") # adverbial_clause_modifier{意外, 余計, そんな}, root{簡単}
adjectival_noun_auxiliary = _add_tag("形状詞-助動詞語幹", "Ana.aux", "adjectival_noun_auxiliary") # auxiliary{よう, そう}, adverbial_clause_modifier{よう}

interjection_filler = _add_tag("感動詞-フィラー", "Interj.fill", "interjection_filler")
interjection_general = _add_tag("感動詞-一般", "Interj.g", "interjection_general") # unspecified_dependency{ううん}

suffix_verbal = _add_tag("接尾辞-動詞的", "Suff.v", "suffix_verbal")
suffix_nominal_verbal_suru = _add_tag("接尾辞-名詞的-サ変可能", "Suff.n.vs", "suffix_nominal_verbal_suru") # root{もの, キス, 連絡}, nominal_modifier{話, 喪失}, nominal_subject{意味}, punctuation{噂}, compound{記憶}, oblique_nominal{ケータイ}, direct_object{衰弱}
suffix_nominal_general = _add_tag("接尾辞-名詞的-一般", "Suff.n.g", "suffix_nominal_general") # nominal_subject{さん}
suffix_nominal_adverbial = _add_tag("接尾辞-名詞的-副詞可能", "Suff.n.adv", "suffix_nominal_adverbial")
suffix_nominal_counter = _add_tag("接尾辞-名詞的-助数詞", "Suff.n.count", "suffix_nominal_counter")
suffix_adjective_i = _add_tag("接尾辞-形容詞的", "Suff.ai", "suffix_adjective_i")
suffix_adjectival_noun = _add_tag("接尾辞-形状詞的", "Suff.ana", "suffix_adjectival_noun")

conjunction = _add_tag("接続詞", "Conj", "conjunction") # coordinating_conjunction{じゃ}

prefix = _add_tag("接頭辞", "Pref", "prefix")

whitespace = _add_tag("空白", "Ws", "whitespace")

symbol_general = _add_tag("記号-一般", "Sym.g", "symbol_general")
symbol_character = _add_tag("記号-文字", "Sym.ch", "symbol_character")

supplementary_symbol_ascii_art_general = _add_tag("補助記号-ＡＡ-一般", "Supsym.aa.g", "supplementary_symbol_ascii_art_general")
supplementary_symbol_ascii_art_emoticon = _add_tag("補助記号-ＡＡ-顔文字", "Supsym.aa.e", "supplementary_symbol_ascii_art_emoticon")
supplementary_symbol_general = _add_tag("補助記号-一般", "Supsym.g", "supplementary_symbol_general")
supplementary_symbol_period = _add_tag("補助記号-句点", "Supsym.p", "supplementary_symbol_period") # punctuation{。}, unspecified_dependency{…}
supplementary_symbol_bracketopen = _add_tag("補助記号-括弧閉", "Supsym.bo", "supplementary_symbol_bracketopen")
supplementary_symbol_bracketclose = _add_tag("補助記号-括弧開", "Supsym.bc", "supplementary_symbol_bracketclose")
supplementary_symbol_comma = _add_tag("補助記号-読点", "Supsym.c", "supplementary_symbol_comma") # punctuation{、}

adnominal = _add_tag("連体詞", "Adn", "adnominal") # determiner{あの, この}
katakana = _add_tag("カタカナ文", "Katakana", "katakana")
chinese_writing = _add_tag("漢文", "Kanbun", "chinese_writing")

hesitation = _add_tag("言いよどみ", "Hesitation", "hesitation")

errors_omissions = _add_tag("web誤脱", "ErrorOmit", "errors_omissions")

dialect = _add_tag("方言", "Dialect", "dialect")

latin_alphabet = _add_tag("ローマ字文", "Lat", "latin_alphabet")

unknown_words = _add_tag("未知語", "Unknown", "unknown_words")
new_unknown_words = _add_tag("新規未知語", "NewUnknown", "new_unknown_words")

foreign_languge = _add_tag("外国語", "foreign_languge", "foreign_languge")