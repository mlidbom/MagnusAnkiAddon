from __future__ import annotations

from typing import TYPE_CHECKING, override

from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from sysutils.weak_ref import WeakRef
from ui.web.sentence.match_viewmodel import MatchViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant

class CandidateWordVariantViewModel:
    def __init__(self, variant: CandidateWordVariant) -> None:
        self.candidate_word: CandidateWordVariant = variant
        self.weakref: WeakRef[CandidateWordVariantViewModel] = WeakRef(self)
        self.is_shadowed: bool = variant.word.is_shadowed
        self.is_display_word: bool = variant in variant.word.analysis.display_word_variants
        self.matches: list[MatchViewModel] = [MatchViewModel(self.weakref, match) for match in variant.matches]
        self.display_matches: list[MatchViewModel] = [match for match in self.matches if match.match.is_displayed]
        self.has_perfect_match: bool = any(match.match_owns_form for match in self.matches if match.match.is_displayed)

        self.primary_display_forms: list[MatchViewModel] = [form for form in self.matches if form.match.is_displayed]
        self.matches = sorted(self.matches, key=lambda match_vm: 0 if match_vm.match.is_displayed else 1)

    @override
    def __repr__(self) -> str: return (
        SkipFalsyValuesDebugReprBuilder()
        .include(self.candidate_word.form)
        .flag("display_word", self.is_display_word)
        .flag("shadowed", self.is_shadowed).repr)
