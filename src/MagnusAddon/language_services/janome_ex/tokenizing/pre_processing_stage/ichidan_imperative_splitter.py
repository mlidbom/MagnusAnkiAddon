from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from language_services.janome_ex.tokenizing.processed_token import ProcessedToken

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_token import JNToken

class IchidanImperativeSplitter(Slots):
    @classmethod
    def try_split(cls, token: JNToken) -> list[ProcessedToken] | None:
        if cls._is_ichidan_imperative(token):
            return cls._split_ichidan_imperative(token)

        return None


    @classmethod
    def _is_ichidan_imperative(cls, token: JNToken) -> bool: return token.inflected_form in InflectionForms.ImperativeMeireikei.ichidan_forms

    @classmethod
    def _split_ichidan_imperative(cls, token: JNToken) -> list[ProcessedToken]:
        ichidan_surface = token.surface[:-1]
        ichidan_imperative_part = token.surface[-1]
        return [ProcessedToken(surface=ichidan_surface, base=token.base_form, is_inflectable_word=True, is_ichidan_imperative_stem=True),
                ProcessedToken(surface=ichidan_imperative_part, base=ichidan_imperative_part, is_inflectable_word=True, is_ichidan_imperative_inflection=True)]
