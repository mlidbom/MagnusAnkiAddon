from parsing.janome_extensions.parts_of_speech import PartsOfSpeech, POS
from sysutils import typed, kana_utils

class TokenExt:
    def __init__(self,
                 parts_of_speech: PartsOfSpeech,
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

    def __eq__(self, other) -> bool:
        if isinstance(other, TokenExt):
            return (self.base_form == other.base_form and
                    self.surface == other.surface and
                    self.inflection_type == other.inflection_type and
                    self.inflected_form == other.inflected_form and
                    #self.reading == other.reading and
                    #self.phonetic == other.phonetic and
                    #self.node_type == other.node_type and
                    self.parts_of_speech == other.parts_of_speech)
        return False

    def is_independent_verb(self) -> bool:
        return self.parts_of_speech == POS.Verb.independent

    def is_verb(self) -> bool:
        return self.parts_of_speech.is_verb()

    def is_verb_auxiliary(self) -> bool:
        return self.parts_of_speech in _verb_auxiliary_parts_of_speech

    def is_adjective(self) -> bool:
        return self.parts_of_speech in _adjective_parts_of_speech

    def is_adjective_auxiliary(self) -> bool:
        return self.parts_of_speech in _adjective_auxiliary_parts_of_speech

_adjective_auxiliary_parts_of_speech = {
    POS.bound_auxiliary, # た, ない past, negation
}

_adjective_parts_of_speech = {
    POS.Adjective.independent,
    POS.Adjective.dependent
}
_verb_auxiliary_parts_of_speech = {
            POS.bound_auxiliary, # た, ない past, negation
            POS.Verb.non_independent, # いる progressive/perfect, いく
            POS.Verb.suffix, # れる passive
            POS.Particle.conjunctive, # て, と
            POS.Particle.coordinating_conjunction, # たり
            POS.Particle.adverbial, # まで todo: not sure about this one
            POS.Adjective.dependent, # よかった
            POS.Noun.NonSelfReliant.general, # こと
            POS.Noun.general
        }