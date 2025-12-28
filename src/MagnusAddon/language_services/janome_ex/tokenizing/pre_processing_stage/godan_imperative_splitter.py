from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from language_services.janome_ex.tokenizing.inflection_types import InflectionTypes
from language_services.janome_ex.tokenizing.processed_token import ProcessedToken

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_token import JNToken

class GodanImperativeSplitter:
    def __init__(self, token: JNToken) -> None:
        self.token: JNToken = token

    def try_split(self) -> list[ProcessedToken] | None:
        if self._is_godan_imperative():
            return self._split_godan_imperative(self.token.base_form)

        return None

    def _is_godan_imperative(self) -> bool:
        if self.token.inflected_form in InflectionForms.ImperativeMeireikei.godan_forms:
            return True

        if (self.token.inflection_type.base == InflectionTypes.Godan.base  # noqa: SIM103
                and self.token.inflected_form == InflectionForms.Hypothetical.general_hypothetical_kateikei
                and self.token.is_end_of_statement()):
            return True

        return False

    def _split_godan_imperative(self, godan_base: str) -> list[ProcessedToken]:
        if self.token.inflected_form == InflectionForms.ImperativeMeireikei.yo:  # handles cases like 放せよ which janome turns into a single token and believes is an ichidan よ imperative
            godan_surface = self.token.surface[:-2]
            imperative_part = self.token.surface[-2]
            return [ProcessedToken(surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_imperative_stem=True),
                    ProcessedToken(surface=imperative_part, base="え", is_inflectable_word=True, is_godan_imperative_inflection=True),
                    ProcessedToken(surface="よ", base="よ", is_inflectable_word=False)]
        elif self.token.inflected_form == InflectionForms.ImperativeMeireikei.ro:  # noqa: RET505
            raise Exception("I doubt this ever happens, but let's explode if it does so we can add support")
        else:  # noqa: RET505
            godan_surface = self.token.surface[:-1]
            imperative_part = self.token.surface[-1]
            imperative_base = "い" if imperative_part == "い" else "え"
            return [ProcessedToken(surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_imperative_stem=True),
                    ProcessedToken(surface=imperative_part, base=imperative_base, is_inflectable_word=True, is_godan_imperative_inflection=True)]
