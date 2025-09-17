from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from ex_autoslot import ProfilableAutoSlots
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.match import Match
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.sentences.sentence_configuration import SentenceConfiguration

class MatchStateTest(WeakRefable, ProfilableAutoSlots):
    def __init__(self, match: WeakRef[Match], name: str, cache_is_in_state: bool) -> None:
        self._match: WeakRef[Match] = match
        self.description: str = name
        self.is_cachable: bool = cache_is_in_state
        weakrefthis = WeakRef(self)
        self.weakref: WeakRef[MatchStateTest] = weakrefthis
        self._future_match_is_in_state: Lazy[bool] | None = Lazy(lambda: weakrefthis()._internal_match_is_in_state()) if cache_is_in_state else None

    @property
    @final
    def match_is_in_state(self) -> bool: return self._future_match_is_in_state() if self._future_match_is_in_state else self._internal_match_is_in_state()

    @property
    def match(self) -> Match: return self._match()
    @property
    def state_description(self) -> str: return self.description
    @property
    def tokenized_form(self) -> str: return self.match.tokenized_form
    @property
    def parsed_form(self) -> str: return self.match.parsed_form
    @property
    def variant(self) -> CandidateWordVariant: return self.match.variant
    @property
    def word(self) -> CandidateWord: return self.variant.word
    @property
    def end_location(self) -> TextAnalysisLocation: return self.word.end_location
    @property
    def configuration(self) -> SentenceConfiguration: return self.variant.configuration
    @property
    def previous_location(self) -> TextAnalysisLocation | None: return self.word.start_location.previous() if self.word.start_location.previous else None
    @property
    def prefix(self) -> str: return self.previous_location.token.surface if self.previous_location else ""
    @property
    def next_location(self) -> TextAnalysisLocation | None: return self.word.end_location.next() if self.word.end_location.next else None
    @property
    def suffix(self) -> str: return self.next_location.token.surface if self.next_location else ""

    def _internal_match_is_in_state(self) -> bool: raise NotImplementedError()

    @override
    def __repr__(self) -> str: return self.state_description
