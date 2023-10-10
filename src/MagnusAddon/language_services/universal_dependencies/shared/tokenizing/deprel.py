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


clausal_modifier_of_noun = _add_tag("acl", "clausal_modifier_of_noun") # https://universaldependencies.org/u/dep/acl.html

relative_clause_modifier = _add_tag("acl:relcl", "relative_clause_modifier") # https://universaldependencies.org/u/dep/acl-relcl.html
adverbial_clause_modifier = _add_tag("advcl", "adverbial_clause_modifier") # https://universaldependencies.org/u/dep/advcl.html

adverbial_modifier = _add_tag("advmod", "adverbial_modifier") # https://universaldependencies.org/u/dep/advmod.html
adverbial_modifier_intensifier = _add_tag("advmod:emph", "adverbial_modifier_intensifier") # https://universaldependencies.org/u/dep/advmod-emph.html
adverbial_modifier_locative = _add_tag("advmod:lmod", "adverbial_modifier_locative") # https://universaldependencies.org/u/dep/advmod-lmod.html

adjectival_modifier = _add_tag("amod", "adjectival_modifier") # https://universaldependencies.org/u/dep/amod.html
appositional_modifier = _add_tag("appos", "appositional_modifier") # https://universaldependencies.org/u/dep/appos.html

auxiliary = _add_tag("aux", "auxiliary") # https://universaldependencies.org/u/dep/aux_.html
auxiliary_passive = _add_tag("aux:pass", "auxiliary_passive") # https://universaldependencies.org/u/dep/aux-pass.html

case_marking = _add_tag("case", "case_marking") # https://universaldependencies.org/u/dep/case.html
coordinating_conjunction = _add_tag("cc", "coordinating_conjunction") # https://universaldependencies.org/u/dep/cc.html
preconjunct = _add_tag("cc:preconj", "preconjunct") # https://universaldependencies.org/u/dep/cc-preconj.html
clausal_complement = _add_tag("ccomp", "clausal_complement") # https://universaldependencies.org/u/dep/ccomp.html
classifier = _add_tag("clf", "classifier") # https://universaldependencies.org/u/dep/clf.html

compound = _add_tag("compound", "compound") # https://universaldependencies.org/u/dep/compound.html
compound_light_verb_construction = _add_tag("compound:lvc", "compound_light_verb_construction") # https://universaldependencies.org/u/dep/compound-lvc.html
compound_phrasal_verb_particle = _add_tag("compound:prt", "compound_phrasal_verb_particle") # https://universaldependencies.org/u/dep/compound-prt.html
compound_reduplicated_compounds = _add_tag("compound:redup", "compound_reduplicated_compounds") # https://universaldependencies.org/u/dep/compound-redup.html
compound_serial_verb_compounds = _add_tag("compound:svc", "compound_serial_verb_compounds") # https://universaldependencies.org/u/dep/compound-svc.html
conjunct = _add_tag("conj", "conjunct") # https://universaldependencies.org/u/dep/conj.html
copula = _add_tag("cop", "copula") # https://universaldependencies.org/u/dep/cop.html
clausal_subject = _add_tag("csubj", "clausal_subject") # https://universaldependencies.org/u/dep/csubj.html
clausal_subject_outer_clause_clausal_subject = _add_tag("csubj:outer", "clausal_subject_outer_clause_clausal_subject") # https://universaldependencies.org/u/dep/csubj-outer.html
clausal_subject_clausal_passive_subject = _add_tag("csubj:pass", "clausal_subject_clausal_passive_subject") # https://universaldependencies.org/u/dep/csubj-pass.html
unspecified_dependency = _add_tag("dep", "unspecified_dependency") # https://universaldependencies.org/u/dep/dep.html

determiner = _add_tag("det", "determiner") # https://universaldependencies.org/u/dep/det.html
determiner_pronominal_quantifier_governing_the_case_of_the_noun = _add_tag("det:numgov", "determiner_pronominal_quantifier_governing_the_case_of_the_noun") # https://universaldependencies.org/u/dep/det-numgov.html
determiner_pronominal_quantifier_agreeing_in_case_with_the_noun = _add_tag("det:nummod", "determiner_pronominal_quantifier_agreeing_in_case_with_the_noun") # https://universaldependencies.org/u/dep/det-nummod.html
determiner_possessive_determiner = _add_tag("det:poss", "determiner_possessive_determiner") # https://universaldependencies.org/u/dep/det-poss.html

discourse_element = _add_tag("discourse", "discourse_element") # https://universaldependencies.org/u/dep/discourse.html
dislocated_elements = _add_tag("dislocated", "dislocated_elements") # https://universaldependencies.org/u/dep/dislocated.html
expletive = _add_tag("expl", "expletive") # https://universaldependencies.org/u/dep/expl.html
expletive_impersonal = _add_tag("expl:impers", "expletive_impersonal") # https://universaldependencies.org/u/dep/expl-impers.html
reflexive_pronoun_used_in_reflexive_passive = _add_tag("expl:pass", "reflexive_pronoun_used_in_reflexive_passive") # https://universaldependencies.org/u/dep/expl-pass.html
reflexive_clitic_with_an_inherently_reflexive_verb = _add_tag("expl:pv", "reflexive_clitic_with_an_inherently_reflexive_verb") # https://universaldependencies.org/u/dep/expl-pv.html

fixed_multiword_expression = _add_tag("fixed", "fixed_multiword_expression") # https://universaldependencies.org/u/dep/fixed.html

flat_multiword_expression = _add_tag("flat", "flat_multiword_expression") # https://universaldependencies.org/u/dep/flat.html
flat_foreign = _add_tag("flat:foreign", "foreign_words") # https://universaldependencies.org/u/dep/flat-foreign.html
flat_name = _add_tag("flat:name", "names") # https://universaldependencies.org/u/dep/flat-name.html
goeswith = _add_tag("goeswith", "goes_with") # https://universaldependencies.org/u/dep/goeswith.html
iobj = _add_tag("iobj", "indirect_object") # https://universaldependencies.org/u/dep/iobj.html
list_ = _add_tag("list", "list") # https://universaldependencies.org/u/dep/list.html
marker = _add_tag("mark", "marker") # https://universaldependencies.org/u/dep/mark.html
nominal_modifier = _add_tag("nmod", "nominal_modifier") # https://universaldependencies.org/u/dep/nmod.html
nmod_poss = _add_tag("nmod:poss", "possessive_nominal_modifier") # https://universaldependencies.org/u/dep/nmod-poss.html
nmod_tmod = _add_tag("nmod:tmod", "temporal_modifier") # https://universaldependencies.org/u/dep/nmod-tmod.html
nominal_subject = _add_tag("nsubj", "nominal_subject") # https://universaldependencies.org/u/dep/nsubj.html
outer_clause_nominal_subject = _add_tag("nsubj:outer", "outer_clause_nominal_subject") # https://universaldependencies.org/u/dep/nsubj-outer.html
passive_nominal_subject = _add_tag("nsubj:pass", "passive_nominal_subject") # https://universaldependencies.org/u/dep/nsubj-pass.html
numeric_modifier = _add_tag("nummod", "numeric_modifier") # https://universaldependencies.org/u/dep/nummod.html
numeric_modifier_governing_the_case_of_the_noun = _add_tag("nummod:gov", "numeric_modifier_governing_the_case_of_the_noun") # https://universaldependencies.org/u/dep/nummod-gov.html
direct_object = _add_tag("obj", "direct_object") # https://universaldependencies.org/u/dep/obj.html
oblique_nominal = _add_tag("obl", "oblique_nominal") # https://universaldependencies.org/u/dep/obl.html
oblique_agent_modifier = _add_tag("obl:agent", "oblique_agent_modifier") # https://universaldependencies.org/u/dep/obl-agent.html
oblique_argument = _add_tag("obl:arg", "oblique_argument") # https://universaldependencies.org/u/dep/obl-arg.html
oblique_locative_modifier = _add_tag("obl:lmod", "oblique_locative_modifier") # https://universaldependencies.org/u/dep/obl-lmod.html
oblique_temporal_modifier = _add_tag("obl:tmod", "oblique_temporal_modifier") # https://universaldependencies.org/u/dep/obl-tmod.html
orphan = _add_tag("orphan", "orphan") # https://universaldependencies.org/u/dep/orphan.html
parataxis = _add_tag("parataxis", "parataxis") # https://universaldependencies.org/u/dep/parataxis.html
punctuation = _add_tag("punct", "punctuation") # https://universaldependencies.org/u/dep/punct.html
reparandum = _add_tag("reparandum", "overridden_disfluency") # https://universaldependencies.org/u/dep/reparandum.html
root = _add_tag("root", "root") # https://universaldependencies.org/u/dep/root.html
vocative = _add_tag("vocative", "vocative") # https://universaldependencies.org/u/dep/vocative.html
open_clausal_complement = _add_tag("xcomp", "open_clausal_complement") # https://universaldependencies.org/u/dep/xcomp.html

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
