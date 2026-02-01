from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

from jastudio.sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from jastudio.sysutils.weak_ref import WeakRef, WeakRefable
from jastudio.ui.web.sentence.match_viewmodel import MatchViewModel

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant

class CandidateWordVariantViewModel(WeakRefable, Slots):
    def __init__(self, variant: CandidateWordVariant) -> None:
        self.candidate_word: CandidateWordVariant = variant
        self.weakref: WeakRef[CandidateWordVariantViewModel] = WeakRef(self)
        self.is_display_word: bool = variant in variant.word.analysis.display_word_variants
        self.matches: list[MatchViewModel] = [MatchViewModel(self.weakref, match) for match in variant.matches]
        self.display_matches: list[MatchViewModel] = [match for match in self.matches if match.match_is_displayed]
        self.has_perfect_match: bool = any(match.match_owns_form for match in self.matches if match.match_is_displayed)

        self.primary_display_forms: list[MatchViewModel] = [form for form in self.matches if form.match_is_displayed]
        self.matches = sorted(self.matches, key=lambda match_vm: 0 if match_vm.match_is_displayed else 1)

    @override
    def __repr__(self) -> str: return (
        SkipFalsyValuesDebugReprBuilder()
        .include(self.candidate_word.form)
        .flag("display_word", self.is_display_word).repr)
