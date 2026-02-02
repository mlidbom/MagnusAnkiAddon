from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from jaslib.language_services.janome_ex.tokenizing.inflection_types import InflectionTypes
from jaslib.language_services.janome_ex.tokenizing.split_token import SplitToken

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
    from jaslib.language_services.janome_ex.tokenizing.jn_token import JNToken

class GodanImperativeSplitter(Slots):
    @classmethod
    def try_split(cls, token: JNToken) -> list[IAnalysisToken] | None:
        if cls._is_godan_imperative(token):
            return cls._split_godan_imperative(token, token.base_form)

        return None

    @classmethod
    def _is_godan_imperative(cls, token: JNToken) -> bool:
        if token.inflected_form in InflectionForms.ImperativeMeireikei.godan_forms:
            return True

        if (token.inflection_type.base == InflectionTypes.Godan.base  # noqa: SIM103
                and token.inflected_form == InflectionForms.Hypothetical.general_hypothetical_kateikei
                and token.is_end_of_statement):
            return True

        return False

    # noinspection DuplicatedCode
    @classmethod
    def _split_godan_imperative(cls, token: JNToken, godan_base: str) -> list[IAnalysisToken]:
        if token.inflected_form == InflectionForms.ImperativeMeireikei.yo:  # handles cases like 放せよ which janome turns into a single token and believes is an ichidan よ imperative
            godan_surface = token.surface[:-2]
            imperative_part = token.surface[-2]
            return [SplitToken(token, surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_imperative_stem=True),
                    SplitToken(token, surface=imperative_part, base="え", is_inflectable_word=True, is_godan_imperative_inflection=True),
                    SplitToken(token, surface="よ", base="よ", is_inflectable_word=False)]
        elif token.inflected_form == InflectionForms.ImperativeMeireikei.ro:  # noqa: RET505
            raise Exception("I doubt this ever happens, but let's explode if it does so we can add support")
        else:  # noqa: RET505
            godan_surface = token.surface[:-1]
            imperative_part = token.surface[-1]
            imperative_base = "い" if imperative_part == "い" else "え"
            return [SplitToken(token, surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_imperative_stem=True),
                    SplitToken(token, surface=imperative_part, base=imperative_base, is_inflectable_word=True, is_godan_imperative_inflection=True)]
