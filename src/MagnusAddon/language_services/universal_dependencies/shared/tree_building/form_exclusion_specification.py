from __future__ import annotations

from typing import Any

from language_services.universal_dependencies.shared.tokenizing.ud_japanese_part_of_speech_tag import UdJapanesePartOfSpeechTag
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken

class FormExclusionSpecification:
    def __init__(self, pos: UdJapanesePartOfSpeechTag, surface: str, lemma:str):
        self.pos = pos
        self.surface = surface
        self.lemma = lemma

    @staticmethod
    def from_token(token: UDToken) -> FormExclusionSpecification: return FormExclusionSpecification(token.xpos, token.form, token.lemma)

    def __eq__(self, other:Any) -> bool: return (isinstance(other, FormExclusionSpecification)
                                                 and other.pos == self.pos
                                                 and other.surface == self.surface
                                                 and other.lemma == self.lemma)

    def __hash__(self) -> int: return hash((self.pos, self.surface, self.lemma))