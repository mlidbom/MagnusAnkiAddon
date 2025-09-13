from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.match import Match
from language_services.janome_ex.word_extraction.matches.requirements.head_requirements import HeadRequirements
from language_services.janome_ex.word_extraction.matches.requirements.in_state import InState
from language_services.janome_ex.word_extraction.matches.requirements.misc_requirements import MiscRequirements
from language_services.janome_ex.word_extraction.matches.requirements.not_in_state import NotInState
from language_services.janome_ex.word_extraction.matches.requirements.requires_forbids_requirement import RequiresForbidsRequirement
from language_services.janome_ex.word_extraction.matches.requirements.tail_requirements import TailRequirements
from language_services.janome_ex.word_extraction.matches.state_tests.another_match_owns_the_form import AnotherMatchOwnsTheForm
from language_services.janome_ex.word_extraction.matches.state_tests.has_a_stem_start import HasAStem
from language_services.janome_ex.word_extraction.matches.state_tests.has_past_tense_stem import HasPastTenseStem
from language_services.janome_ex.word_extraction.matches.state_tests.has_prefix import PrefixIsIn
from language_services.janome_ex.word_extraction.matches.state_tests.has_te_form_stem import HasTeFormStem
from language_services.janome_ex.word_extraction.matches.state_tests.is_sentence_start import IsSentenceStart
from language_services.janome_ex.word_extraction.matches.state_tests.yield_to_following_overlapping_compound import YieldToFollowingOverlappingCompound
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote import VocabNote
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration

@final
class VocabMatch(Match, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], vocab: VocabNote) -> None:
        super().__init__(word_variant,
                         validity_requirements=[
                             NotInState(AnotherMatchOwnsTheForm(self)),
                             # head reqiuirements
                             NotInState(PrefixIsIn(self, vocab.matching_configuration.configurable_rules.prefix_is_not.get(), true_if_no_prefixes=False)),
                             InState(PrefixIsIn(self, vocab.matching_configuration.configurable_rules.required_prefix.get(), true_if_no_prefixes=True)),
                             RequiresForbidsRequirement(IsSentenceStart(self), vocab.matching_configuration.requires_forbids.sentence_start),
                             RequiresForbidsRequirement(HasTeFormStem(self), vocab.matching_configuration.requires_forbids.te_form_stem),
                             RequiresForbidsRequirement(HasAStem(self), vocab.matching_configuration.requires_forbids.a_stem),
                             RequiresForbidsRequirement(HasPastTenseStem(self), vocab.matching_configuration.requires_forbids.past_tense_stem)
                         ],
                         display_requirements=[
                             NotInState(YieldToFollowingOverlappingCompound(self))
                         ])
        self.vocab: VocabNote = vocab
        self.word_variant: WeakRef[CandidateWordVariant] = word_variant
        self.weakref = WeakRef(self)

        self.head_requirements: HeadRequirements = HeadRequirements(self, word_variant, self.word_variant().word.start_location.previous)
        self.tail_requirements: TailRequirements = TailRequirements(self.vocab, self.word_variant().word.end_location.next)
        self.misc_requirements: MiscRequirements = MiscRequirements(self.weakref)

    @property
    def matching(self) -> VocabNoteMatchingConfiguration: return self.vocab.matching_configuration
    @property
    @override
    def match_form(self) -> str: return self.vocab.get_question()
    @property
    @override
    def answer(self) -> str: return self.vocab.get_answer()
    @property
    @override
    def readings(self) -> list[str]: return self.vocab.readings.get()

    @property
    @override
    def parsed_form(self) -> str:
        return self.vocab.question.raw \
            if self.matching.bool_flags.question_overrides_form.is_set() \
            else super().parsed_form

    @property
    @override
    def start_index(self) -> int:
        if (self.matching.bool_flags.question_overrides_form.is_set()
                and self.matching.configurable_rules.required_prefix.any()):
            matched_prefixes = [prefix for prefix in self.matching.configurable_rules.required_prefix.get()
                                if self.parsed_form.startswith(prefix)]
            if matched_prefixes:
                matched_prefix_length = max(len(prefix) for prefix in matched_prefixes)
                return super().start_index - matched_prefix_length

        return super().start_index

    @property
    @override
    def _is_valid_internal(self) -> bool:
        return (super()._is_valid_internal
                and self.head_requirements.are_fulfilled
                and self.tail_requirements.are_fulfilled
                and self.misc_requirements.are_fulfilled)

    @property
    @override
    def is_secondary_match(self) -> bool: return not self.owns_form and self._another_match_owns_form

    @property
    def _another_match_owns_form(self) -> bool: return any(other_match for other_match in self.word_variant().vocab_matches
                                                           if other_match != self
                                                           and other_match.owns_form
                                                           and other_match.is_valid)

    @property
    def owns_form(self) -> bool: return self.vocab.forms.is_owned_form(self.tokenized_form)

    @property
    @override
    def failure_reasons(self) -> list[str]:
        return (super().failure_reasons
                + self.misc_requirements.failure_reasons()
                + self.head_requirements.failure_reasons()
                + self.tail_requirements.failure_reasons())

    @override
    def __repr__(self) -> str: return f"""{self.vocab.get_question()}, {self.vocab.get_answer()[:10]}: {" ".join(self.failure_reasons)} {" ".join(self.hiding_reasons)}"""
