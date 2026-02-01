from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jastudio.language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from jastudio.language_services.janome_ex.tokenizing.split_token import SplitToken

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
    from jastudio.language_services.janome_ex.tokenizing.jn_token import JNToken

class IchidanImperativeSplitter(Slots):
    @classmethod
    def try_split(cls, token: JNToken) -> list[IAnalysisToken] | None:
        if cls._is_ichidan_imperative(token):
            return cls._split_ichidan_imperative(token)

        return None

    @classmethod
    def _is_ichidan_imperative(cls, token: JNToken) -> bool: return token.inflected_form in InflectionForms.ImperativeMeireikei.ichidan_forms

    @classmethod
    def _split_ichidan_imperative(cls, token: JNToken) -> list[IAnalysisToken]:
        ichidan_surface = token.surface[:-1]
        ichidan_imperative_part = token.surface[-1]
        return [SplitToken(token, surface=ichidan_surface, base=token.base_form, is_inflectable_word=True, is_ichidan_imperative_stem=True),
                SplitToken(token, surface=ichidan_imperative_part, base=ichidan_imperative_part, is_inflectable_word=True, is_ichidan_imperative_inflection=True)]
