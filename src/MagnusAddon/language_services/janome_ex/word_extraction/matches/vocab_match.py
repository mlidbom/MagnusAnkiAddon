from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.match import Match
from language_services.janome_ex.word_extraction.matches.requirements.in_state import InState
from language_services.janome_ex.word_extraction.matches.requirements.not_in_state import NotInState
from language_services.janome_ex.word_extraction.matches.requirements.requires_forbids_requirement import RequiresForbidsRequirement
from language_services.janome_ex.word_extraction.matches.state_tests.another_match_owns_the_form import AnotherMatchOwnsTheForm
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_a_stem import HasAStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_e_stem import HasEStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_past_tense_stem import HasPastTenseStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_te_form_stem import HasTeFormStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.is_sentence_start import IsSentenceStart
from language_services.janome_ex.word_extraction.matches.state_tests.head.prefix_is_in import PrefixIsIn
from language_services.janome_ex.word_extraction.matches.state_tests.is_exact_match import IsExactMatch
from language_services.janome_ex.word_extraction.matches.state_tests.is_poison_word import IsPoisonWord
from language_services.janome_ex.word_extraction.matches.state_tests.is_single_token import IsSingleToken
from language_services.janome_ex.word_extraction.matches.state_tests.surface_is_in import SurfaceIsIn
from language_services.janome_ex.word_extraction.matches.state_tests.tail.has_overlapping_following_compound import HasOverlappingFollowingCompound
from language_services.janome_ex.word_extraction.matches.state_tests.tail.is_sentence_end import IsSentenceEnd
from language_services.janome_ex.word_extraction.matches.state_tests.tail.suffix_is_in import SuffixIsIn
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote import VocabNote
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration

@final
class VocabMatch(Match, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], vocab: VocabNote) -> None:
        self.weakref = WeakRef(self)
        super().__init__(word_variant,
                         validity_requirements=[
                             NotInState(AnotherMatchOwnsTheForm(self.weakref)),
                             # head requirements
                             NotInState(PrefixIsIn(self.weakref, vocab.matching_configuration.configurable_rules.prefix_is_not.get()),
                                        is_requirement_active=vocab.matching_configuration.configurable_rules.prefix_is_not.any()),
                             InState(PrefixIsIn(self.weakref, vocab.matching_configuration.configurable_rules.required_prefix.get()),
                                     is_requirement_active=vocab.matching_configuration.configurable_rules.required_prefix.any()),
                             RequiresForbidsRequirement(IsSentenceStart(self.weakref), vocab.matching_configuration.requires_forbids.sentence_start),
                             RequiresForbidsRequirement(HasTeFormStem(self.weakref), vocab.matching_configuration.requires_forbids.te_form_stem),
                             RequiresForbidsRequirement(HasAStem(self.weakref), vocab.matching_configuration.requires_forbids.a_stem),
                             RequiresForbidsRequirement(HasPastTenseStem(self.weakref), vocab.matching_configuration.requires_forbids.past_tense_stem),
                             RequiresForbidsRequirement(HasEStem(self.weakref), vocab.matching_configuration.requires_forbids.e_stem),

                             # tail requirements
                             RequiresForbidsRequirement(IsSentenceEnd(self.weakref), vocab.matching_configuration.requires_forbids.sentence_end),
                             NotInState(SuffixIsIn(self.weakref, vocab.matching_configuration.configurable_rules.suffix_is_not.get()),
                                        is_requirement_active=vocab.matching_configuration.configurable_rules.suffix_is_not.any()),

                             # misc requirements
                             NotInState(IsPoisonWord(self.weakref)),
                             RequiresForbidsRequirement(IsExactMatch(self.weakref), vocab.matching_configuration.requires_forbids.exact_match),
                             RequiresForbidsRequirement(IsSingleToken(self.weakref), vocab.matching_configuration.requires_forbids.single_token),
                             NotInState(SurfaceIsIn(self.weakref, vocab.matching_configuration.configurable_rules.surface_is_not.get()),
                                        is_requirement_active=vocab.matching_configuration.configurable_rules.surface_is_not.any()),
                             NotInState(SurfaceIsIn(self.weakref, vocab.matching_configuration.configurable_rules.yield_to_surface.get()),
                                        is_requirement_active=vocab.matching_configuration.configurable_rules.yield_to_surface.any()),
                         ],
                         display_requirements=[
                             NotInState(HasOverlappingFollowingCompound(self.weakref),
                                        is_requirement_active=vocab.matching_configuration.requires_forbids.yield_last_token.is_required)
                         ])
        self.vocab: VocabNote = vocab
        self.word_variant: WeakRef[CandidateWordVariant] = word_variant

    @property
    def matching_configuration(self) -> VocabNoteMatchingConfiguration: return self.vocab.matching_configuration
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
            if self.matching_configuration.bool_flags.question_overrides_form.is_set() \
            else super().parsed_form

    @property
    @override
    def start_index(self) -> int:
        if (self.matching_configuration.bool_flags.question_overrides_form.is_set()
                and self.matching_configuration.configurable_rules.required_prefix.any()):
            matched_prefixes = [prefix for prefix in self.matching_configuration.configurable_rules.required_prefix.get()
                                if self.parsed_form.startswith(prefix)]
            if matched_prefixes:
                matched_prefix_length = max(len(prefix) for prefix in matched_prefixes)
                return super().start_index - matched_prefix_length

        return super().start_index

    @override
    def __repr__(self) -> str: return f"""{self.vocab.get_question()}, {self.vocab.get_answer()[:10]}: {" ".join(self.failure_reasons)} {" ".join(self.hiding_reasons)}"""
