from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.tokenizing import inflection_forms, inflection_types
from language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
from language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from language_services.janome_ex.tokenizing.inflection_types import InflectionTypes
from language_services.janome_ex.tokenizing.jn_parts_of_speech import JNPOS, JNPartsOfSpeech
from language_services.janome_ex.word_extraction import analysis_constants
from sysutils import kana_utils, typed
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from janome.tokenizer import Token  # pyright: ignore[reportMissingTypeStubs]
    from language_services.janome_ex.tokenizing.inflection_forms import InflectionForm
    from language_services.janome_ex.tokenizing.inflection_types import InflectionType

# noinspection PyUnusedFunction
class JNToken(IAnalysisToken, WeakRefable, Slots):
    SPLITTER_TOKEN_TEXT: str = "removethissplittertoken"
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
        self.weak_ref: WeakRef[JNToken] = WeakRef(self)
        self._base_form: str = typed.str_(base_form)
        self._surface: str = typed.str_(surface)
        self.inflection_type: InflectionType = inflection_types.all_dict[inflection_type] if isinstance(inflection_type, str) else inflection_type
        self.inflected_form: InflectionForm = inflection_forms.all_dict[inflected_form] if isinstance(inflected_form, str) else inflected_form
        self.reading: str = typed.str_(reading)
        self.phonetic: str = typed.str_(phonetic)
        self.node_type: str = typed.str_(node_type)
        self.parts_of_speech: JNPartsOfSpeech = parts_of_speech
        self.raw_token: Token | None = raw_token
        self._previous: WeakRef[JNToken] | None = None
        self._next: WeakRef[JNToken] | None = None

    @property
    def next(self) -> JNToken | None: return self._next() if self._next else None
    @property
    def previous(self) -> JNToken | None: return self._previous() if self._previous else None

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

    # <IAnalysisToken implementation>
    @property
    @override
    def is_past_tense_stem(self) -> bool: return self.inflected_form == InflectionForms.Continuative.ta_connection  # "連用タ接続"
    @property
    @override
    def is_ichidan_masu_stem(self) -> bool: return self.is_masu_stem  # todo why is this checking for any masu stem and not checking anything ichidan specific?
    _te_connections: set[InflectionForm] = {InflectionForms.Continuative.te_connection, InflectionForms.Continuative.de_connection}
    @property
    @override
    def is_te_form_stem(self) -> bool:
        return (self.inflected_form in JNToken._te_connections or
                (self.is_past_tense_stem and self.surface.endswith("ん")))
    @property
    @override
    def is_past_tense_marker(self) -> bool: return self.inflection_type == InflectionTypes.Special.ta  # "連用タ接続"
    @property
    @override
    def is_special_nai_negative(self) -> bool: return self.inflection_type == InflectionTypes.Special.nai
    @property
    @override
    def is_masu_stem(self) -> bool: return (self.inflected_form == InflectionForms.Continuative.renyoukei_masu_stem
                                            and self.is_verb())
    @property
    @override
    def is_adverb(self) -> bool:
        return (self.parts_of_speech == JNPOS.Adverb.general
                or (self.parts_of_speech in JNPOS.Adjective.all_types and self.surface.endswith("く")))
    @property
    @override
    def surface(self) -> str: return self._surface
    @property
    @override
    def base_form(self) -> str: return self._base_form
    _pseudo_verbs_for_inflection_purposes: set[str] = {"ます"}
    @property
    @override
    def is_inflectable_word(self) -> bool:
        return self.is_verb() or self.is_adjective() or self.base_form in self._pseudo_verbs_for_inflection_purposes
    @property
    @override
    def is_non_word_character(self) -> bool: return self.parts_of_speech.is_non_word_character()

    @property
    @override
    def is_a_stem(self) -> bool: return self.is_godan_verb() and self.inflected_form in InflectionForms.Irrealis.all_forms
    # </IAnalysisToken implementation>

    def is_verb(self) -> bool:
        return self.parts_of_speech in JNPOS.Verb.all_types

    def is_adjective(self) -> bool:
        return self.parts_of_speech in JNPOS.Adjective.all_types

    def is_ichidan_verb(self) -> bool:
        return self.inflection_type.base == InflectionTypes.Ichidan.base

    _actually_suru_verbs_not_godan: set[str] = {"する", "為る"}
    def is_godan_verb(self) -> bool:
        return self.inflection_type.base == InflectionTypes.Godan.base and self.base_form not in JNToken._actually_suru_verbs_not_godan

    @property
    def is_kuru_verb(self) -> bool:
        return self.inflection_type.base == InflectionTypes.Kahen.base

    @property
    def is_suru_verb(self) -> bool:
        return self.inflection_type.base == InflectionTypes.Sahen.base or self.base_form in JNToken._actually_suru_verbs_not_godan

    def is_dictionary_form(self) -> bool:
        return self.inflected_form == InflectionForms.Basic.dictionary_form

    _te_forms: set[str] = {"て", "って", "で"}
    @property
    def is_te_form(self) -> bool:
        return (self.parts_of_speech == JNPOS.Particle.conjunctive
                and self.surface in JNToken._te_forms)

    # _deru_te_form_roots: set[str] = {"ん", "い"}
    _something_something: set[str] = {"でる", "どる"}
    def is_progressive_form(self) -> bool:
        return (self.surface == "てる"
                or (self.surface in JNToken._something_something and self.previous is not None and self.previous.inflected_form == InflectionForms.Continuative.ta_connection)
                or (self.surface == "いる" and self.previous is not None and self.previous.is_te_form))

    def is_t_form_marker(self) -> bool:
        return self.inflection_type == InflectionTypes.Special.ta  # "連用タ接続"

    def is_end_of_statement(self) -> bool:
        return (self.next is None
                or self.next.parts_of_speech == JNPOS.Particle.sentence_ending
                or self.next.surface in analysis_constants.sentence_end_characters
                or self.next.is_non_word_character)

    _invalid_ichidan_inflection_surfaces: set[str] = {"っ"}
    def cannot_follow_ichidan_stem(self) -> bool:
        return self.surface in JNToken._invalid_ichidan_inflection_surfaces

    _pos_more_likely_to_follow_imperative_than_ichidan_stem: set[JNPartsOfSpeech] = set()
    def is_more_likely_to_follow_imperative_than_ichidan_stem(self) -> bool:
        if self.parts_of_speech.is_noun():
            return True
        return self.parts_of_speech in JNToken._pos_more_likely_to_follow_imperative_than_ichidan_stem

    _valid_potential_form_inflections_pos: set[JNPartsOfSpeech] = {JNPOS.bound_auxiliary, JNPOS.Noun.Suffix.auxiliary_verb_stem, JNPOS.Verb.dependent, JNPOS.Particle.conjunctive, JNPOS.Particle.coordinating_conjunction}
    _invalid_godan_potential_form_surfaces: set[str] = {"っ"}
    def is_valid_godan_potential_form_inflection(self) -> bool:
        if self.parts_of_speech in self._valid_potential_form_inflections_pos:  # noqa: SIM102, SIM103
            if self.surface not in JNToken._invalid_godan_potential_form_surfaces:
                return True
        return False
