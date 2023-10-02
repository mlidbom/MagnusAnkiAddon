class UdUniversalPartOfSpeechTag:
    def __init__(self, tag: str, description: str):
        self.tag = tag
        self.description = description

    def __str__(self) -> str: return self.description


def get_tag(tag:str) -> UdUniversalPartOfSpeechTag:
    return _tag_dictionary[tag]


_tag_dictionary: dict[str, UdUniversalPartOfSpeechTag] = {}

def _add_tag(tag:str, description:str) -> UdUniversalPartOfSpeechTag:
    created_tag = UdUniversalPartOfSpeechTag(tag, description)
    _tag_dictionary[tag] = created_tag
    return created_tag

adjective = _add_tag("ADJ", "adjective")
adposition = _add_tag("ADP", "adposition(suffix/prefix)")
adverb = _add_tag("ADV", "adverb")
auxiliary = _add_tag("AUX", "auxiliary")
conjunction_coordinating = _add_tag("CCONJ", "conjunction_coordinating")
conjunction_subordinating = _add_tag("SCONJ", "conjunction_subordinating")
determiner = _add_tag("DET", "determiner")
interjection = _add_tag("INTJ", "interjection")
noun = _add_tag("NOUN", "noun")
noun_proper = _add_tag("PROPN", "noun_proper")
noun_pronoun = _add_tag("PRON", "noun_pronoun")

numeral = _add_tag("NUM", "numeral")
particle = _add_tag("PART", "particle")
punctuation = _add_tag("PUNCT", "punctuation")
symbol = _add_tag("SYM", "symbol")
verb = _add_tag("VERB", "verb")
other = _add_tag("X", "other")










# From: https://universaldependencies.org/u/pos/index.html
# ADJ: adjective
# ADP: adposition
# ADV: adverb
# AUX: auxiliary
# CCONJ: coordinating conjunction
# DET: determiner
# INTJ: interjection
# NOUN: noun
# NUM: numeral
# PART: particle
# PRON: pronoun
# PROPN: proper noun
# PUNCT: punctuation
# SCONJ: subordinating conjunction
# SYM: symbol
# VERB: verb
# X: other