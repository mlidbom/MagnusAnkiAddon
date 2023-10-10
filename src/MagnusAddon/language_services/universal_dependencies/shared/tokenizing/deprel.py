# From: https://universaldependencies.org/u/dep/index.html

"""deprel is the relationship between a token and the token's head"""
class UdRelationshipTag:
    def __init__(self, tag: str, description: str) -> None:
        self.tag = tag
        self.description = description

    def __str__(self) -> str: return self.description


_tag_to_tag_dict: dict[str, UdRelationshipTag] = dict()


def get_tag(tag: str) -> UdRelationshipTag:
    return _tag_to_tag_dict[tag]


def _add_tag(tag: str, description: str) -> UdRelationshipTag:
    tag_object = UdRelationshipTag(tag, description)
    _tag_to_tag_dict[tag] = tag_object
    return tag_object

# verb_bound{する, 行き},
# adjective_i_general{素晴らしい},
# verb_general{知っ, 捨てる, 振り, 持っ, 食べ}
clausal_modifier_of_noun = _add_tag("acl", "clausal_modifier_of_noun") # https://universaldependencies.org/u/dep/acl.html

# verb_general{出, 言え, 調べ, 思っ, 書く, 聞か, 言わ, 誘っ, 言っ},
# adjective_i_general{明るい},
# adjective_i_bound{いい, 良く},
# adjectival_noun_general{余計, 意外, そんな},
# adjectival_noun_auxiliary{よう},
# verb_bound{来, 得る, い, やっ, 忘れ, なる},
# noun_common_general{友達}, adverb{ああ}
adverbial_clause_modifier = _add_tag("advcl", "adverbial_clause_modifier") # https://universaldependencies.org/u/dep/advcl.html

# adverb{そう, ついに, とりあえず, どう, なぜ, もう, ちゃんと},
# noun_common_general{ダメダメ},
# noun_common_adverbial{絶対, 朝, 普段, 全部}
adverbial_modifier = _add_tag("advmod", "adverbial_modifier") # https://universaldependencies.org/u/dep/advmod.html

# inflecting_dependent_word{られる, ちゃう, られ, て, せ, だ, とい, な, ない, なく, てる, た, なかっ, たら, で, たい, なら, らしい, れる, に},
# adjectival_noun_auxiliary{そう, よう},
# verb_bound{する, し}
auxiliary = _add_tag("aux", "auxiliary") # https://universaldependencies.org/u/dep/aux_.html

# https://universaldependencies.org/u/dep/case.html
# particle_case_marking{と, へ, じゃ, から, で, が, を, の, に},
# particle_binding{は, も},
# particle_adverbial{まで, か, って}
case_marking = _add_tag("case", "case_marking")

# inflecting_dependent_word{だっ},
# conjunction{じゃ}
coordinating_conjunction = _add_tag("cc", "coordinating_conjunction") # https://universaldependencies.org/u/dep/cc.html

# verb_bound{ある},
# adjective_i_bound{よかっ}
clausal_complement = _add_tag("ccomp", "clausal_complement") # https://universaldependencies.org/u/dep/ccomp.html

# noun_common_general{かっこ, こと, 神経}, particle_adverbial{ばっか},
# noun_proper_name_surname{藤宮},
# noun_proper_place_general{日代},
# noun_common_verbal_suru{記憶},
# noun_numeral{二千九百}
compound = _add_tag("compound", "compound") # https://universaldependencies.org/u/dep/compound.html

# inflecting_dependent_word{じゃ, でし, だっ, だ, に}
copula = _add_tag("cop", "copula") # https://universaldependencies.org/u/dep/cop.html

# interjection_general{ううん},
# particle_case_marking{と},
# supplementary_symbol_period{…}
unspecified_dependency = _add_tag("dep", "unspecified_dependency") # https://universaldependencies.org/u/dep/dep.html

# noun_common_adjectival{無表情}
adjectival_modifier = _add_tag("amod", "adjectival_modifier") # https://universaldependencies.org/u/dep/amod.html

# particle_binding{も},
# adjective_i_bound{いい, ない},
# particle_case_marking{に, が},
# verb_bound{もらえ, おけ, ある, し, いく, くれ, いる},
# inflecting_dependent_word{たら, だ, です}
fixed_multiword_expression = _add_tag("fixed", "fixed_multiword_expression") # https://universaldependencies.org/u/dep/fixed.html

# particle_conjunctive{と, ば, けど, し, て, から, ちゃ},
# particle_adverbial{か, って, まで, たり},
# particle_phrase_final{な, か, ね, よ, ぞ, じゃん},
# particle_nominal{ん, の},
# inflecting_dependent_word{ん}
marker = _add_tag("mark", "marker") # https://universaldependencies.org/u/dep/mark.html

# noun_common_adverbial{今, 前, 相変わらず},
# noun_common_general{自分},
# noun_common_verbal_suru{喪失, 話},
# noun_pronoun{俺}
nominal_modifier = _add_tag("nmod", "nominal_modifier") # https://universaldependencies.org/u/dep/nmod.html

# noun_common_general{気, こと, 町, やつ, 自分, 友達},
# suffix_nominal_general{さん},
# noun_pronoun{あいつ, 俺},
# noun_common_verbal_suru{意味}
nominal_subject = _add_tag("nsubj", "nominal_subject") # https://universaldependencies.org/u/dep/nsubj.html

# noun_common_general{日記, 近所, 夢, こと},
# noun_common_adjectival{楽},
# noun_pronoun{私},
# noun_common_verbal_suru{衰弱}
direct_object = _add_tag("obj", "direct_object") # https://universaldependencies.org/u/dep/obj.html

# noun_common_adverbial{夜, 所, 中, 一度, 時, 以外},
# verb_bound{いる},
# noun_common_general{気, 先生, ごめん, 日記, 態度, 自分, 自宅, 女性, 本題, ご飯},
# noun_pronoun{いつ, 何, そっち, これ, 私},
# noun_common_verbal_suru{ケータイ}
oblique_nominal = _add_tag("obl", "oblique_nominal") # https://universaldependencies.org/u/dep/obl.html

# verb_general{気づか, 知ら, 逃げ, 思う, 聞い, 逢え, 助け, いう, 会う, 入る, 当て, 食べよう, 探し, 読ん, 離れ, 食べ, 言っ},
# noun_common_verbal_suru{キス, 連絡, もの}, verb_bound{あげる, 行こう, なっ, する, 行っ, 見, くる, やろう, あり},
# adjective_i_bound{良かっ, なかっ, いい, ない, よかっ, 良けれ},
# noun_common_adverbial{ため},
# noun_common_general{ホント, 放課後, 人},
# inflecting_dependent_word{だっ, だろう},
# particle_case_marking{と},
# adverb{やっぱり, ぶらぶら},
# noun_pronoun{何},
# adjective_i_general{偉},
# noun_common_adjectival{ダメ},
# adjectival_noun_general{簡単},
# noun_common_counter{円}
root = _add_tag("root", "root") # https://universaldependencies.org/u/dep/root.html

# supplementary_symbol_period{。}, supplementary_symbol_comma{、}, noun_common_verbal_suru{噂}
punctuation = _add_tag("punct", "punctuation") #  https://universaldependencies.org/u/dep/punct.html



relative_clause_modifier = _add_tag("acl:relcl", "relative_clause_modifier") # https://universaldependencies.org/u/dep/acl-relcl.html
adverbial_modifier_intensifier = _add_tag("advmod:emph", "adverbial_modifier_intensifier") # https://universaldependencies.org/u/dep/advmod-emph.html
adverbial_modifier_locative = _add_tag("advmod:lmod", "adverbial_modifier_locative") # https://universaldependencies.org/u/dep/advmod-lmod.html
appositional_modifier = _add_tag("appos", "appositional_modifier") # https://universaldependencies.org/u/dep/appos.html
auxiliary_passive = _add_tag("aux:pass", "auxiliary_passive") # https://universaldependencies.org/u/dep/aux-pass.html
preconjunct = _add_tag("cc:preconj", "preconjunct") # https://universaldependencies.org/u/dep/cc-preconj.html
classifier = _add_tag("clf", "classifier") # https://universaldependencies.org/u/dep/clf.html
compound_light_verb_construction = _add_tag("compound:lvc", "compound_light_verb_construction") # https://universaldependencies.org/u/dep/compound-lvc.html
compound_phrasal_verb_particle = _add_tag("compound:prt", "compound_phrasal_verb_particle") # https://universaldependencies.org/u/dep/compound-prt.html
compound_reduplicated_compounds = _add_tag("compound:redup", "compound_reduplicated_compounds") # https://universaldependencies.org/u/dep/compound-redup.html
compound_serial_verb_compounds = _add_tag("compound:svc", "compound_serial_verb_compounds") # https://universaldependencies.org/u/dep/compound-svc.html
conjunct = _add_tag("conj", "conjunct") # https://universaldependencies.org/u/dep/conj.html
clausal_subject = _add_tag("csubj", "clausal_subject") # https://universaldependencies.org/u/dep/csubj.html
clausal_subject_outer_clause_clausal_subject = _add_tag("csubj:outer", "clausal_subject_outer_clause_clausal_subject") # https://universaldependencies.org/u/dep/csubj-outer.html
clausal_subject_clausal_passive_subject = _add_tag("csubj:pass", "clausal_subject_clausal_passive_subject") # https://universaldependencies.org/u/dep/csubj-pass.html
determiner = _add_tag("det", "determiner") # adnominal{この, あの}  https://universaldependencies.org/u/dep/det.html
determiner_pronominal_quantifier_governing_the_case_of_the_noun = _add_tag("det:numgov", "determiner_pronominal_quantifier_governing_the_case_of_the_noun") # https://universaldependencies.org/u/dep/det-numgov.html
determiner_pronominal_quantifier_agreeing_in_case_with_the_noun = _add_tag("det:nummod", "determiner_pronominal_quantifier_agreeing_in_case_with_the_noun") # https://universaldependencies.org/u/dep/det-nummod.html
determiner_possessive_determiner = _add_tag("det:poss", "determiner_possessive_determiner") # https://universaldependencies.org/u/dep/det-poss.html
discourse_element = _add_tag("discourse", "discourse_element") # https://universaldependencies.org/u/dep/discourse.html
dislocated_elements = _add_tag("dislocated", "dislocated_elements") # https://universaldependencies.org/u/dep/dislocated.html
expletive = _add_tag("expl", "expletive") # https://universaldependencies.org/u/dep/expl.html
expletive_impersonal = _add_tag("expl:impers", "expletive_impersonal") # https://universaldependencies.org/u/dep/expl-impers.html
reflexive_pronoun_used_in_reflexive_passive = _add_tag("expl:pass", "reflexive_pronoun_used_in_reflexive_passive") # https://universaldependencies.org/u/dep/expl-pass.html
reflexive_clitic_with_an_inherently_reflexive_verb = _add_tag("expl:pv", "reflexive_clitic_with_an_inherently_reflexive_verb") # https://universaldependencies.org/u/dep/expl-pv.html
flat_multiword_expression = _add_tag("flat", "flat_multiword_expression") # https://universaldependencies.org/u/dep/flat.html
flat_foreign = _add_tag("flat:foreign", "foreign_words") # https://universaldependencies.org/u/dep/flat-foreign.html
flat_name = _add_tag("flat:name", "names") # https://universaldependencies.org/u/dep/flat-name.html
goeswith = _add_tag("goeswith", "goes_with") # https://universaldependencies.org/u/dep/goeswith.html
iobj = _add_tag("iobj", "indirect_object") # https://universaldependencies.org/u/dep/iobj.html
list_ = _add_tag("list", "list") # https://universaldependencies.org/u/dep/list.html
nmod_poss = _add_tag("nmod:poss", "possessive_nominal_modifier") # https://universaldependencies.org/u/dep/nmod-poss.html
nmod_tmod = _add_tag("nmod:tmod", "temporal_modifier") # https://universaldependencies.org/u/dep/nmod-tmod.html
outer_clause_nominal_subject = _add_tag("nsubj:outer", "outer_clause_nominal_subject") # https://universaldependencies.org/u/dep/nsubj-outer.html
passive_nominal_subject = _add_tag("nsubj:pass", "passive_nominal_subject") # https://universaldependencies.org/u/dep/nsubj-pass.html
numeric_modifier = _add_tag("nummod", "numeric_modifier") # https://universaldependencies.org/u/dep/nummod.html
numeric_modifier_governing_the_case_of_the_noun = _add_tag("nummod:gov", "numeric_modifier_governing_the_case_of_the_noun") # https://universaldependencies.org/u/dep/nummod-gov.html
oblique_agent_modifier = _add_tag("obl:agent", "oblique_agent_modifier") # https://universaldependencies.org/u/dep/obl-agent.html
oblique_argument = _add_tag("obl:arg", "oblique_argument") # https://universaldependencies.org/u/dep/obl-arg.html
oblique_locative_modifier = _add_tag("obl:lmod", "oblique_locative_modifier") # https://universaldependencies.org/u/dep/obl-lmod.html
oblique_temporal_modifier = _add_tag("obl:tmod", "oblique_temporal_modifier") # https://universaldependencies.org/u/dep/obl-tmod.html
orphan = _add_tag("orphan", "orphan") # https://universaldependencies.org/u/dep/orphan.html
parataxis = _add_tag("parataxis", "parataxis") # https://universaldependencies.org/u/dep/parataxis.html
reparandum = _add_tag("reparandum", "overridden_disfluency") # https://universaldependencies.org/u/dep/reparandum.html
vocative = _add_tag("vocative", "vocative") # https://universaldependencies.org/u/dep/vocative.html
open_clausal_complement = _add_tag("xcomp", "open_clausal_complement") # https://universaldependencies.org/u/dep/xcomp.html