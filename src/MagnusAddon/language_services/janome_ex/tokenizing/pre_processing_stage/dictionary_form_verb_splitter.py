from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.tokenizing.godan_dictionary_form_stem import GodanDictionaryFormInflection, GodanDictionaryFormStem, IchidanDictionaryFormInflection, IchidanDictionaryFormStem, KuruVerbDictionaryFormInflection, KuruVerbDictionaryFormStem, SuruVerbDictionaryFormInflection, SuruVerbDictionaryFormStem

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
    from language_services.janome_ex.tokenizing.jn_token import JNToken

class DictionaryFormVerbSplitter(Slots):
    @classmethod
    def try_split(cls, token: JNToken) -> list[IAnalysisToken] | None:
        if token.is_dictionary_form() and not token.is_progressive_form():
            if token.is_ichidan_verb:
                return cls.split_ichidan_dictionary_form(token)

            if token.is_godan_verb:
                return cls.split_godan_dictionary_form(token)

            if token.is_kuru_verb:
                return cls.split_kuru_verb(token)

            if token.is_suru_verb:
                return cls.split_suru_verb(token)

        return None

    @classmethod
    def split_ichidan_dictionary_form(cls, token: JNToken) -> list[IAnalysisToken]:
        ichidan_surface = token.surface[:-1]
        return [IchidanDictionaryFormStem(token, surface=ichidan_surface, base=token.base_form),
                IchidanDictionaryFormInflection(token)]

    @classmethod
    def split_godan_dictionary_form(cls, token: JNToken) -> list[IAnalysisToken]:
        godan_surface = token.surface[:-1]
        godan_dictionary_ending = token.surface[-1]
        return [GodanDictionaryFormStem(token, surface=godan_surface, base=token.base_form),
                GodanDictionaryFormInflection(token, surface=godan_dictionary_ending, base="う")]

    @classmethod
    def split_kuru_verb(cls, token: JNToken) -> list[IAnalysisToken]:
        surface = token.surface[:-1]
        return [KuruVerbDictionaryFormStem(token, surface=surface, base=token.base_form),
                KuruVerbDictionaryFormInflection(token)]

    @classmethod
    def split_suru_verb(cls, token: JNToken) -> list[IAnalysisToken]:
        surface = token.surface[:-1]
        return [SuruVerbDictionaryFormStem(token, surface=surface, base=token.base_form),
                SuruVerbDictionaryFormInflection(token)]
