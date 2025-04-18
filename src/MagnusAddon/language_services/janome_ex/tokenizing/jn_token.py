from typing import Any

from language_services.janome_ex.tokenizing.jn_parts_of_speech import JNPartsOfSpeech, POS
from sysutils import typed, kana_utils

#I want to keep this around for now. I think It might be used reconsider if you see this much later 2024-11-16
# noinspection PyUnusedFunction
class JNToken:
    def __init__(self,
                 parts_of_speech: JNPartsOfSpeech,
                 base_form: str,
                 surface: str,
                 inflection_type: str = "",
                 inflected_form: str = "",
                 reading: str = "",
                 phonetic: str = "",
                 node_type: str = ""):
        self.base_form = typed.str_(base_form)
        self.surface = typed.str_(surface)
        self.inflection_type = typed.str_(inflection_type).replace("*", "")
        self.inflected_form = typed.str_(inflected_form).replace("*", "")
        self.reading = typed.str_(reading)
        self.phonetic = typed.str_(phonetic)
        self.node_type = typed.str_(node_type)
        self.parts_of_speech = parts_of_speech

    def __repr__(self) -> str:
        return "".join([
            "TokenExt(",
            "" + kana_utils.pad_to_length(f"'{self.base_form}'", 6),
            ", " + kana_utils.pad_to_length(f"'{self.surface}'", 6),
            ", " + kana_utils.pad_to_length(f"'{self.inflection_type}'", 6),
            ", " + kana_utils.pad_to_length(f"'{self.inflected_form}'", 10),
            #", " + kana_utils.pad_to_length(f"'{self.reading}'", 10),
            #", " + kana_utils.pad_to_length(f"'{self.phonetic}'", 10),
            #", " + kana_utils.pad_to_length(f"'{self.node_type}'", 10),
            ", " + str(self.parts_of_speech)])

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, JNToken):
            return (self.base_form == other.base_form and
                    self.surface == other.surface and
                    self.inflection_type == other.inflection_type and
                    self.inflected_form == other.inflected_form and
                    #self.reading == other.reading and
                    #self.phonetic == other.phonetic and
                    #self.node_type == other.node_type and
                    self.parts_of_speech == other.parts_of_speech)
        return False

    def is_verb(self) -> bool:
        return self.parts_of_speech in _verb_parts_of_speech

    def is_verb_auxiliary(self) -> bool:
        return self.parts_of_speech in _verb_auxiliary_parts_of_speech

    def is_adjective(self) -> bool:
        return self.parts_of_speech in _adjective_parts_of_speech

    def is_adjective_auxiliary(self) -> bool:
        if self.parts_of_speech in _adjective_auxiliary_parts_of_speech:
            return True

        if self.inflection_type == "サ変・スル" and self.inflected_form == "連用形": # irregular conjugations of する like し
            return True

        return False


    def is_noun(self) -> bool:
        if self.parts_of_speech in _noun_parts_of_speech:
            return True
        return False

    def is_inflected_verb(self) -> bool:
        return self.parts_of_speech.is_verb() and self.inflected_form == "連用タ接続"

    def is_noun_auxiliary(self) -> bool:
        return self.parts_of_speech in _noun_auxiliary_parts_of_speech

    def is_end_of_phrase_particle(self) -> bool:
        if self.parts_of_speech in _end_of_phrase_particles:
            return True

        if self.parts_of_speech == POS.Particle.conjunctive and self.surface != "て":
            return True

        return False

    _verb_inflection_token_surfaces = set(["て", "てる", "た", "たら"])
    _verb_inflection_token_bases = set(["れる", "られる", "ちゃう"])
    def is_verb_inflection_word(self) -> bool:
        return (self.surface in self._verb_inflection_token_surfaces
                or self.base_form in self._verb_inflection_token_bases)

_end_of_phrase_particles = {
    POS.Particle.CaseMarking.general,
    POS.Particle.CaseMarking.compound,
    POS.Particle.CaseMarking.quotation,
    POS.Particle.adverbial # まで : this feels strange, but works so far.
}

_noun_parts_of_speech = {
    POS.Noun.general, # 自分
    POS.Noun.Pronoun.general, # あいつ
    POS.Noun.suru_verb, # 話
    POS.Noun.adverbial, # 今
    POS.Noun.na_adjective_stem # 余慶
}

_adjective_auxiliary_parts_of_speech = {
    POS.bound_auxiliary, # た, ない past, negation
    POS.Particle.conjunctive, # て,と,し
    #POS.Adverb.general, # もう
}

_adjective_parts_of_speech = {
    POS.Adjective.independent,
    POS.Adjective.dependent
}

_noun_auxiliary_parts_of_speech = {
    POS.Noun.general, # 自分

    POS.Particle.CaseMarking.general, # が
    POS.Particle.adnominalization, # の
    POS.Particle.binding, # は
    POS.Noun.Dependent.adverbial, # なか
    POS.Noun.Dependent.general, # こと
    POS.Particle.adverbial,  # まで
    POS.Particle.adverbialization # に
} | _adjective_parts_of_speech | _adjective_auxiliary_parts_of_speech

_verb_parts_of_speech = {
    POS.Verb.independent,
    POS.Verb.dependent, #todo: this seems odd
    POS.Verb.suffix #todo: this seems odd
}

_verb_auxiliary_parts_of_speech = {
            POS.bound_auxiliary, # た, ない past, negation
            POS.Particle.binding, # は, も
            POS.Particle.sentence_ending, # な
            POS.Verb.dependent, # いる progressive/perfect, いく
            POS.Verb.suffix, # れる passive
            POS.Particle.conjunctive, # て,と,し
            POS.Particle.coordinating_conjunction, # たり
            POS.Particle.adverbial, # まで todo: not sure about this one
            POS.Adjective.dependent, # よかった
            POS.Adjective.independent, # ない
            POS.Noun.Dependent.general, # こと
            POS.Noun.general
        } | _verb_parts_of_speech