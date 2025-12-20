from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.tokenizing import inflection_forms, inflection_types
from language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from language_services.janome_ex.tokenizing.inflection_types import InflectionTypes
from language_services.janome_ex.tokenizing.jn_parts_of_speech import POS, JNPartsOfSpeech
from language_services.janome_ex.word_extraction import analysis_constants
from manually_copied_in_libraries.autoslot import Slots
from sysutils import kana_utils, typed

if TYPE_CHECKING:
    from janome.tokenizer import Token  # pyright: ignore[reportMissingTypeStubs]
    from language_services.janome_ex.tokenizing.inflection_forms import InflectionForm
    from language_services.janome_ex.tokenizing.inflection_types import InflectionType

# noinspection PyUnusedFunction
class JNToken(Slots):
    def __init__(self,
                 parts_of_speech: JNPartsOfSpeech,
                 base_form: str,
                 surface: str,
                 inflection_type: str | InflectionType = "*",
                 inflected_form: str | InflectionForm = "*",
                 reading: str = "",
                 phonetic: str = "",
                 node_type: str = "",
                 raw_token: Token | None = None) -> None:
        self.base_form: str = typed.str_(base_form)
        self.surface: str = typed.str_(surface)
        self.inflection_type: InflectionType = inflection_types.all_dict[inflection_type] if isinstance(inflection_type, str) else inflection_type
        self.inflected_form: InflectionForm = inflection_forms.all_dict[inflected_form] if isinstance(inflected_form, str) else inflected_form
        self.reading: str = typed.str_(reading)
        self.phonetic: str = typed.str_(phonetic)
        self.node_type: str = typed.str_(node_type)
        self.parts_of_speech: JNPartsOfSpeech = parts_of_speech
        self.raw_token: Token | None = raw_token
        self.previous: JNToken | None = None
        self.next: JNToken | None = None

    @override
    def __repr__(self) -> str:
        return "".join([
            "JNToken(",
            "" + kana_utils.pad_to_length(f"'{self.base_form}'", 6),
            ", " + kana_utils.pad_to_length(f"'{self.surface}'", 6),
            ", " + kana_utils.pad_to_length(f"'{self.inflection_type}'", 6),
            ", " + kana_utils.pad_to_length(f"'{self.inflected_form}'", 10),
            # ", " + kana_utils.pad_to_length(f"'{self.reading}'", 10),
            # ", " + kana_utils.pad_to_length(f"'{self.phonetic}'", 10),
            # ", " + kana_utils.pad_to_length(f"'{self.node_type}'", 10),
            ", " + str(self.parts_of_speech)])

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, JNToken):
            return (self.base_form == other.base_form and
                    self.surface == other.surface and
                    self.inflection_type == other.inflection_type and
                    self.inflected_form == other.inflected_form and
                    # self.reading == other.reading and
                    # self.phonetic == other.phonetic and
                    # self.node_type == other.node_type and
                    self.parts_of_speech == other.parts_of_speech)
        return False

    def is_verb(self) -> bool:
        return self.parts_of_speech in _verb_parts_of_speech

    _pseudo_verbs_for_inflection_purposes: set[str] = {"ます"}
    def is_inflectable_word(self) -> bool:
        return self.is_verb() or self.is_adjective() or self.base_form in self._pseudo_verbs_for_inflection_purposes

    def is_verb_auxiliary(self) -> bool:
        return self.parts_of_speech in _verb_auxiliary_parts_of_speech

    def is_adjective(self) -> bool:
        return self.parts_of_speech in _adjective_parts_of_speech

    def is_adjective_auxiliary(self) -> bool:
        if self.parts_of_speech in _adjective_auxiliary_parts_of_speech:
            return True

        return self.inflection_type == InflectionTypes.Sahen.suru and self.inflected_form == InflectionForms.Continuative.renyoukei_masu_stem  # "連用形" # irregular conjugations of する like し # "サ変・スル"

    def is_ichidan_verb(self) -> bool:
        return self.inflection_type == InflectionTypes.Ichidan.regular

    def is_noun(self) -> bool:
        return self.parts_of_speech in _noun_parts_of_speech

    def is_past_tense_stem(self) -> bool:
        return self.inflected_form == InflectionForms.Continuative.ta_connection  # "連用タ接続"

    _te_connections: set[InflectionForm] = {InflectionForms.Continuative.te_connection, InflectionForms.Continuative.de_connection}
    def is_te_form_stem(self) -> bool:
        return (self.inflected_form in JNToken._te_connections or
                (self.is_past_tense_stem() and self.surface.endswith("ん")))

    def is_ichidan_masu_stem(self) -> bool:
        return self.inflected_form == InflectionForms.Continuative.renyoukei_masu_stem

    def is_special_nai_negative(self) -> bool:
        return self.inflection_type == InflectionTypes.Special.nai

    def is_past_tense_marker(self) -> bool:
        return self.inflection_type == InflectionTypes.Special.ta  # "連用タ接続"

    def is_t_form_marker(self) -> bool:
        return self.inflection_type == InflectionTypes.Special.ta  # "連用タ接続"

    def is_noun_auxiliary(self) -> bool:
        return self.parts_of_speech in _noun_auxiliary_parts_of_speech

    def is_end_of_statement(self) -> bool:
        return self.next is None or self.next.surface in analysis_constants.sentence_end_characters or self.parts_of_speech.is_non_word_character()

    _valid_potential_form_inflections_pos: set[JNPartsOfSpeech] = {POS.bound_auxiliary, POS.Noun.Suffix.auxiliary_verb_stem}
    def is_valid_potential_form_inflection(self) -> bool:
        if self.parts_of_speech in self._valid_potential_form_inflections_pos:  # noqa: SIM103
            return True
        return False

    def is_end_of_phrase_particle(self) -> bool:
        if self.parts_of_speech in _end_of_phrase_particles:
            return True

        return self.parts_of_speech == POS.Particle.conjunctive and self.surface != "て"

_end_of_phrase_particles = {
    POS.Particle.CaseMarking.general,
    POS.Particle.CaseMarking.compound,
    POS.Particle.CaseMarking.quotation,
    POS.Particle.adverbial  # まで : this feels strange, but works so far.
}

_noun_parts_of_speech = {
    POS.Noun.general,  # 自分
    POS.Noun.Pronoun.general,  # あいつ
    POS.Noun.suru_verb,  # 話
    POS.Noun.adverbial,  # 今
    POS.Noun.na_adjective_stem  # 余慶
}

_adjective_auxiliary_parts_of_speech = {
    POS.bound_auxiliary,  # た, ない past, negation
    POS.Particle.conjunctive,  # て,と,し
    # POS.Adverb.general, # もう
}

_adjective_parts_of_speech = {
    POS.Adjective.independent,
    POS.Adjective.dependent
}

_noun_auxiliary_parts_of_speech = {
                                      POS.Noun.general,  # 自分

                                      POS.Particle.CaseMarking.general,  # が
                                      POS.Particle.adnominalization,  # の
                                      POS.Particle.binding,  # は
                                      POS.Noun.Dependent.adverbial,  # なか
                                      POS.Noun.Dependent.general,  # こと
                                      POS.Particle.adverbial,  # まで
                                      POS.Particle.adverbialization  # に
                                  } | _adjective_parts_of_speech | _adjective_auxiliary_parts_of_speech

_verb_parts_of_speech = {
    POS.Verb.independent,
    POS.Verb.dependent,
    POS.Verb.suffix
}

_verb_auxiliary_parts_of_speech = {
                                      POS.bound_auxiliary,  # た, ない past, negation
                                      POS.Particle.binding,  # は, も
                                      POS.Particle.sentence_ending,  # な
                                      POS.Verb.dependent,  # いる progressive/perfect, いく
                                      POS.Verb.suffix,  # れる passive
                                      POS.Particle.conjunctive,  # て,と,し
                                      POS.Particle.coordinating_conjunction,  # たり
                                      POS.Particle.adverbial,  # まで
                                      POS.Adjective.dependent,  # よかった
                                      POS.Adjective.independent,  # ない
                                      POS.Noun.Dependent.general,  # こと
                                      POS.Noun.general
                                  } | _verb_parts_of_speech
