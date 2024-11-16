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

# noinspection PyUnusedClass, PyUnusedName
class UDPOS:
    adjective = _add_tag("ADJ", "adjective") # https://universaldependencies.org/ja/pos/ADJ.html
    adposition = _add_tag("ADP", "adposition(suffix/prefix)") # https://universaldependencies.org/ja/pos/ADP.html
    adverb = _add_tag("ADV", "adverb") # https://universaldependencies.org/ja/pos/ADV.html
    auxiliary = _add_tag("AUX", "auxiliary") # https://universaldependencies.org/ja/pos/AUX_.html
    conjunction_coordinating = _add_tag("CCONJ", "conjunction_coordinating") # https://universaldependencies.org/ja/pos/CCONJ.html
    conjunction_subordinating = _add_tag("SCONJ", "conjunction_subordinating") # https://universaldependencies.org/ja/pos/SCONJ.html
    determiner = _add_tag("DET", "determiner") # https://universaldependencies.org/ja/pos/DET.html
    interjection = _add_tag("INTJ", "interjection") # https://universaldependencies.org/ja/pos/INTJ.html
    noun = _add_tag("NOUN", "noun") # https://universaldependencies.org/ja/pos/NOUN.html
    noun_proper = _add_tag("PROPN", "noun_proper") # https://universaldependencies.org/ja/pos/PROPN.html
    noun_pronoun = _add_tag("PRON", "noun_pronoun") # https://universaldependencies.org/ja/pos/PRON.html

    numeral = _add_tag("NUM", "numeral") # https://universaldependencies.org/ja/pos/NUM.html
    particle = _add_tag("PART", "particle") # https://universaldependencies.org/ja/pos/PART.html
    punctuation = _add_tag("PUNCT", "punctuation") # https://universaldependencies.org/ja/pos/PUNCT.html
    symbol = _add_tag("SYM", "symbol") # https://universaldependencies.org/ja/pos/SYM.html
    verb = _add_tag("VERB", "verb") # https://universaldependencies.org/ja/pos/VERB.html
    other = _add_tag("X", "other") # https://universaldependencies.org/ja/pos/X.html










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