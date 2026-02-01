from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.language_services.janome_ex.word_extraction.matches.match import Match
from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.generic_forbids import Forbids

if TYPE_CHECKING:
    from collections.abc import Callable

    from jastudio.language_services.jamdict_ex.dict_entry import DictEntry
    from jastudio.language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
    from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement
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

    _requirements_list: list[Callable[[MatchInspector], FailedMatchRequirement | None]] = [
            # new style
            Forbids("dict_match_with_dictionary_form_stem", lambda it: it.start_location_is_dictionary_verb_inflection).apply_to,
    ]

    _combined_requirements: list[Callable[[MatchInspector], FailedMatchRequirement | None]] = Match._match_primary_validity_requirements + _requirements_list

    @override
    def _is_primarily_valid(self) -> bool:
        inspector = self.inspector
        return not any(failure for failure in (requirement(inspector) for requirement in DictionaryMatch._combined_requirements) if failure is not None)

    @override
    def _create_primary_validity_failures(self) -> list[FailedMatchRequirement]:
        inspector = self.inspector
        return [failure for failure in (requirement(inspector) for requirement in DictionaryMatch._combined_requirements) if failure is not None]
