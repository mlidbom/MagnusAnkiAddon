from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from language_services.janome_ex.tokenizing.processed_token import ProcessedToken

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_token import JNToken

class IchidanImperativeSplitter:
    def __init__(self, token: JNToken) -> None:
        self.token: JNToken = token

    def try_split(self) -> list[ProcessedToken] | None:
        if self._is_ichidan_imperative():
            return self._split_ichidan_imperative()

        return None

    def _is_ichidan_imperative(self) -> bool: return self.token.inflected_form in InflectionForms.ImperativeMeireikei.ichidan_forms

    def _split_ichidan_imperative(self) -> list[ProcessedToken]:
        ichidan_surface = self.token.surface[:-1]
        ichidan_imperative_part = self.token.surface[-1]
        return [ProcessedToken(surface=ichidan_surface, base=self.token.base_form, is_inflectable_word=True, is_ichidan_imperative_stem=True),
                ProcessedToken(surface=ichidan_imperative_part, base=ichidan_imperative_part, is_inflectable_word=True, is_ichidan_imperative_inflection=True)]
