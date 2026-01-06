from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.tokenizing.godan_dictionary_form_stem import GodanDictionaryFormInflection, GodanDictionaryFormStem, IchidanDictionaryFormInflection, IchidanDictionaryFormStem

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
    from language_services.janome_ex.tokenizing.jn_token import JNToken

class DictionaryFormVerbSplitter(Slots):
    @classmethod
    def try_split(cls, token: JNToken) -> list[IAnalysisToken] | None:
        if token.is_ichidan_verb() and token.is_dictionary_form() and not token.is_progressive_form():
            return cls.try_split_ichidan_dictionary_form(token)

        if token.is_godan_verb() and token.is_dictionary_form() and not token.is_progressive_form():
            return cls.try_split_godan_dictionary_form(token)

        return None

    @classmethod
    def try_split_ichidan_dictionary_form(cls, token: JNToken) -> list[IAnalysisToken] | None:
        ichidan_surface = token.surface[:-1]
        return [IchidanDictionaryFormStem(token, surface=ichidan_surface, base=token.base_form),
                IchidanDictionaryFormInflection(token, surface="る")]

    @classmethod
    def try_split_godan_dictionary_form(cls, token: JNToken) -> list[IAnalysisToken] | None:
        godan_surface = token.surface[:-1]
        godan_dictionary_ending = token.surface[-1]
        return [GodanDictionaryFormStem(token, surface=godan_surface, base=token.base_form),
                GodanDictionaryFormInflection(token, surface=godan_dictionary_ending, base="う")]
