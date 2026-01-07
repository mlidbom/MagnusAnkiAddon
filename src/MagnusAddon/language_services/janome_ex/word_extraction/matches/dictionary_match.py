from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.match import Match

if TYPE_CHECKING:
    from language_services.jamdict_ex.dict_entry import DictEntry
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement
    from sysutils.weak_ref import WeakRef

class DictionaryMatch(Match, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], dictionary_entry: DictEntry) -> None:
        super().__init__(word_variant)
        self.dictionary_entry: DictEntry = dictionary_entry

    @property
    @override
    def answer(self) -> str: return self.dictionary_entry.format_answer()
    @property
    @override
    def readings(self) -> list[str]: return self.dictionary_entry.kana_forms_text()

    @override
    def _create_display_requirements(self) -> tuple[MatchRequirement | None, ...]: return ()
    @override
    def _create_primary_validity_failures(self) -> list[FailedMatchRequirement | None]: return []
    @override
    def _create_interdependent_validity_failures(self) -> tuple[FailedMatchRequirement | None, ...]: return ()
