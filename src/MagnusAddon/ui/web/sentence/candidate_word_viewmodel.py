from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from sysutils.weak_ref import WeakRef
from ui.web.sentence.display_form_viewmodel import DisplayFormViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWordVariant


class CandidateWordViewModel:
    def __init__(self, candidate_word: CandidateWordVariant) -> None:
        self.candidate_word: CandidateWordVariant = candidate_word
        self.weakref: WeakRef[CandidateWordViewModel] = WeakRef(self)
        self.is_shadowed: bool = candidate_word.is_shadowed
        self.is_display_word: bool = candidate_word in candidate_word.token_range().analysis().display_words
        self.display_forms: list[DisplayFormViewModel] = [DisplayFormViewModel(self.weakref, form) for form in candidate_word.display_forms]
        self.has_perfect_match = any(form.is_perfect_match for form in self.display_forms)

    def __repr__(self) -> str: return (
        SkipFalsyValuesDebugReprBuilder()
        .include(self.candidate_word.form)
        .flag("display_word", self.is_display_word)
        .flag("shadowed", self.is_shadowed).repr)
