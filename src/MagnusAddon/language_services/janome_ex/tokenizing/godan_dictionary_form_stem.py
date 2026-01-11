from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_token import JNToken

# this is the interface that is actually used in the text analysis pipeline

class SplitTokenBase(IAnalysisToken, Slots):
    def __init__(self,
                 source: JNToken,
                 surface: str,
                 base: str) -> None:
        self.source: JNToken = source
        self._surface: str = surface
        self._base_form: str = base

    @property
    @override
    def source_token(self) -> JNToken: return self.source
    @property
    @override
    def surface(self) -> str: return self._surface
    @property
    @override
    def base_form(self) -> str: return self._base_form

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.surface}', '{self.base_form}')"

class GodanDictionaryFormStem(SplitTokenBase, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

    @property
    @override
    def is_dictionary_verb_form_stem(self) -> bool: return True

class GodanDictionaryFormInflection(SplitTokenBase, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

    @property
    @override
    def is_dictionary_verb_inflection(self) -> bool: return True

class IchidanDictionaryFormStem(SplitTokenBase, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

    @property
    @override
    def is_dictionary_verb_form_stem(self) -> bool: return True

class IchidanDictionaryFormInflection(SplitTokenBase, Slots):
    def __init__(self, source: JNToken) -> None:
        super().__init__(source, "る", "る")

    @property
    @override
    def is_dictionary_verb_inflection(self) -> bool: return True

class KuruVerbDictionaryFormStem(SplitTokenBase, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

    @property
    @override
    def is_dictionary_verb_form_stem(self) -> bool: return True

class KuruVerbDictionaryFormInflection(SplitTokenBase, Slots):
    def __init__(self, source: JNToken) -> None:
        super().__init__(source, "る", "る")

    @property
    @override
    def is_dictionary_verb_inflection(self) -> bool: return True

class SuruVerbDictionaryFormStem(SplitTokenBase, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

    @property
    @override
    def is_dictionary_verb_form_stem(self) -> bool: return True

class SuruVerbDictionaryFormInflection(SplitTokenBase, Slots):
    def __init__(self, source: JNToken) -> None:
        super().__init__(source, "る", "る")

    @property
    @override
    def is_dictionary_verb_inflection(self) -> bool: return True
