from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots
from language_services import conjugator
from sysutils import kana_utils
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration
    from sysutils.weak_ref import WeakRef

@final
class HeadRequirements(Slots):
    def __init__(self, match: VocabMatch, word_variant: WeakRef[CandidateWordVariant], end_of_stem: WeakRef[TextAnalysisLocation] | None) -> None:
        rules: VocabNoteMatchingConfiguration = match.vocab.matching_configuration
        self.config: VocabNoteMatchingConfiguration = rules

        self.has_past_tense_stem: bool = end_of_stem is not None and (end_of_stem().token.is_past_tense_stem() or word_variant().word.start_location.token.is_past_tense_marker())
        self.fulfills_forbids_past_tense_stem: bool = not rules.requires_forbids.past_tense_stem.is_forbidden or not self.has_past_tense_stem
        self.fulfills_requires_past_tense_stem: bool = not rules.requires_forbids.past_tense_stem.is_required or self.has_past_tense_stem

        self.has_e_stem: bool = (end_of_stem is not None and
                                 (end_of_stem().token.surface[-1] in conjugator.e_stem_characters
                                  or kana_utils.character_is_kanji(end_of_stem().token.surface[-1])))

        self.fulfills_requires_e_stem_requirement: bool = not rules.requires_forbids.e_stem.is_required or self.has_e_stem
        self.fulfills_forbids_e_stem_requirement: bool = not rules.requires_forbids.e_stem.is_forbidden or not self.has_e_stem

        self.are_fulfilled = (True
                              and self.fulfills_requires_e_stem_requirement
                              and self.fulfills_forbids_e_stem_requirement
                              and self.fulfills_requires_past_tense_stem
                              and self.fulfills_forbids_past_tense_stem
                              )

    def failure_reasons(self) -> list[str]:
        return (SimpleStringListBuilder()
                .append_if(not self.fulfills_forbids_e_stem_requirement, "forbids_e_stem")
                .append_if(not self.fulfills_requires_e_stem_requirement, "requires_e_stem")
                .append_if(not self.fulfills_forbids_past_tense_stem, "forbids_past_tense_stem")
                .append_if(not self.fulfills_requires_past_tense_stem, "requires_past_tense_stem")
                .value)

    @override
    def __repr__(self) -> str: return " ".join(self.failure_reasons())
