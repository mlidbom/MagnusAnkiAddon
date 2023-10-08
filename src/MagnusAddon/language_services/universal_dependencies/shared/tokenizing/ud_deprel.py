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


clausal_modifier_of_noun = _add_tag("acl", "clausal_modifier_of_noun")
relative_clause_modifier = _add_tag("acl:relcl", "relative_clause_modifier")
adverbial_clause_modifier = _add_tag("advcl", "adverbial_clause_modifier")
adverbial_modifier = _add_tag("advmod", "adverbial_modifier")
advmod_emph = _add_tag("advmod:emph", "emphasizing_word_intensifier")
advmod_lmod = _add_tag("advmod:lmod", "locative_adverbial_modifier")
amod = _add_tag("amod", "adjectival_modifier")
appos = _add_tag("appos", "appositional_modifier")
aux = _add_tag("aux", "auxiliary")
aux_pass = _add_tag("aux:pass", "passive_auxiliary")
case_marking = _add_tag("case", "case_marking")
cc = _add_tag("cc", "coordinating_conjunction")
cc_preconj = _add_tag("cc:preconj", "preconjunct")
ccomp = _add_tag("ccomp", "clausal_complement")
clf = _add_tag("clf", "classifier")
compound = _add_tag("compound", "compound")
compound_lvc = _add_tag("compound:lvc", "light_verb_construction")
compound_prt = _add_tag("compound:prt", "phrasal_verb_particle")
compound_redup = _add_tag("compound:redup", "reduplicated_compounds")
compound_svc = _add_tag("compound:svc", "serial_verb_compounds")
conj = _add_tag("conj", "conjunct")
cop = _add_tag("cop", "copula")
csubj = _add_tag("csubj", "clausal_subject")
csubj_outer = _add_tag("csubj:outer", "outer_clause_clausal_subject")
csubj_pass = _add_tag("csubj:pass", "clausal_passive_subject")
dep = _add_tag("dep", "unspecified_dependency")
det = _add_tag("det", "determiner")
det_numgov = _add_tag("det:numgov", "pronominal_quantifier_governing_the_case_of_the_noun")
det_nummod = _add_tag("det:nummod", "pronominal_quantifier_agreeing_in_case_with_the_noun")
det_poss = _add_tag("det:poss", "possessive_determiner")
discourse = _add_tag("discourse", "discourse_element")
dislocated = _add_tag("dislocated", "dislocated_elements")
expl = _add_tag("expl", "expletive")
expl_impers = _add_tag("expl:impers", "impersonal_expletive")
expl_pass = _add_tag("expl:pass", "reflexive_pronoun_used_in_reflexive_passive")
expl_pv = _add_tag("expl:pv", "reflexive_clitic_with_an_inherently_reflexive_verb")
fixed = _add_tag("fixed", "fixed_multiword_expression")
flat = _add_tag("flat", "flat_multiword_expression")
flat_foreign = _add_tag("flat:foreign", "foreign_words")
flat_name = _add_tag("flat:name", "names")
goeswith = _add_tag("goeswith", "goes_with")
iobj = _add_tag("iobj", "indirect_object")
list_ = _add_tag("list", "list")
mark = _add_tag("mark", "marker")
nmod = _add_tag("nmod", "nominal_modifier")
nmod_poss = _add_tag("nmod:poss", "possessive_nominal_modifier")
nmod_tmod = _add_tag("nmod:tmod", "temporal_modifier")
nsubj = _add_tag("nsubj", "nominal_subject")
nsubj_outer = _add_tag("nsubj:outer", "outer_clause_nominal_subject")
nsubj_pass = _add_tag("nsubj:pass", "passive_nominal_subject")
nummod = _add_tag("nummod", "numeric_modifier")
nummod_gov = _add_tag("nummod:gov", "numeric_modifier_governing_the_case_of_the_noun")
direct_object = _add_tag("obj", "direct_object")
obl = _add_tag("obl", "oblique_nominal")
obl_agent = _add_tag("obl:agent", "agent_modifier")
obl_arg = _add_tag("obl:arg", "oblique_argument")
obl_lmod = _add_tag("obl:lmod", "locative_modifier")
obl_tmod = _add_tag("obl:tmod", "temporal_modifier")
orphan = _add_tag("orphan", "orphan")
parataxis = _add_tag("parataxis", "parataxis")
punct = _add_tag("punct", "punctuation")
reparandum = _add_tag("reparandum", "overridden_disfluency")
root = _add_tag("root", "root")
vocative = _add_tag("vocative", "vocative")
xcomp = _add_tag("xcomp", "open_clausal_complement")

# From: https://universaldependencies.org/u/dep/index.html
# acl: clausal modifier of noun (adnominal clause)
# acl:relcl: relative clause modifier
# advcl: adverbial clause modifier
# advmod: adverbial modifier
# advmod:emph: emphasizing word,intensifier
# advmod:lmod: locative adverbial modifier
# amod: adjectival modifier
# appos: appositional modifier
# aux: auxiliary
# aux:pass: passive auxiliary
# case: case marking
# cc: coordinating conjunction
# cc:preconj: preconjunct
# ccomp: clausal complement
# clf: classifier
# compound: compound
# compound:lvc: light verb construction
# compound:prt: phrasal verb particle
# compound:redup: reduplicated compounds
# compound:svc: serial verb compounds
# conj: conjunct
# cop: copula
# csubj: clausal subject
# csubj:outer: outer clause clausal subject
# csubj:pass: clausal passive subject
# dep: unspecified dependency
# det: determiner
# det:numgov: pronominal quantifier governing the case of the noun
# det:nummod: pronominal quantifier agreeing in case with the noun
# det:poss: possessive determiner
# discourse: discourse element
# dislocated: dislocated elements
# expl: expletive
# expl:impers: impersonal expletive
# expl:pass: reflexive pronoun used in reflexive passive
# expl:pv: reflexive clitic with an inherently reflexive verb
# fixed: fixed multiword expression
# flat: flat multiword expression
# flat:foreign: foreign words
# flat:name: names
# goeswith: goes with
# iobj: indirect object
# list: list
# mark: marker
# nmod: nominal modifier
# nmod:poss: possessive nominal modifier
# nmod:tmod: temporal modifier
# nsubj: nominal subject
# nsubj:outer: outer clause nominal subject
# nsubj:pass: passive nominal subject
# nummod: numeric modifier
# nummod:gov: numeric modifier governing the case of the noun
# obj: object
# obl: oblique nominal
# obl:agent: agent modifier
# obl:arg: oblique argument
# obl:lmod: locative modifier
# obl:tmod: temporal modifier
# orphan: orphan
# parataxis: parataxis
# punct: punctuation
# reparandum: overridden disfluency
# root: root
# vocative: vocative
# xcomp: open clausal complement
