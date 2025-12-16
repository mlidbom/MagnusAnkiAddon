from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from ex_autoslot import AutoSlots
from language_services.janome_ex.word_extraction.matches.match import Match
from language_services.janome_ex.word_extraction.matches.requirements.forbids_state import Forbids
from language_services.janome_ex.word_extraction.matches.requirements.requires_forbids_requirement import RequiresOrForbids
from language_services.janome_ex.word_extraction.matches.requirements.requires_state import Requires
from language_services.janome_ex.word_extraction.matches.state_tests.another_match_owns_the_form import AnotherMatchOwnsTheForm
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_a_stem import HasAStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_e_stem import HasEStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_past_tense_stem import HasPastTenseStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_te_form_stem import HasTeFormStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.is_sentence_start import IsSentenceStart
from language_services.janome_ex.word_extraction.matches.state_tests.head.prefix_is_in import PrefixIsIn
from language_services.janome_ex.word_extraction.matches.state_tests.is_exact_match import IsExactMatch
from language_services.janome_ex.word_extraction.matches.state_tests.is_godan_imperative import IsGodanImperative
from language_services.janome_ex.word_extraction.matches.state_tests.is_godan_potential import IsGodanPotential
from language_services.janome_ex.word_extraction.matches.state_tests.is_poison_word import IsPoisonWord
from language_services.janome_ex.word_extraction.matches.state_tests.is_single_token import IsSingleToken
from language_services.janome_ex.word_extraction.matches.state_tests.surface_is_in import SurfaceIsIn
from language_services.janome_ex.word_extraction.matches.state_tests.tail.has_overlapping_following_compound import HasDisplayedOverlappingFollowingCompound
from language_services.janome_ex.word_extraction.matches.state_tests.tail.is_sentence_end import IsSentenceEnd
from language_services.janome_ex.word_extraction.matches.state_tests.tail.suffix_is_in import SuffixIsIn
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote import VocabNote
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration

@final
class VocabMatch(Match, AutoSlots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], vocab: VocabNote) -> None:
        weakref: WeakRef[VocabMatch] = WeakRef(self)
        self.requires_forbids = vocab.matching_configuration.requires_forbids
        self.rules = vocab.matching_configuration.configurable_rules
        super().__init__(word_variant,
                         validity_requirements=[
                             Forbids(AnotherMatchOwnsTheForm(weakref)),
                             # head requirements
                             Forbids(PrefixIsIn(weakref, self.rules.prefix_is_not.get()),
                                     is_requirement_active=self.rules.prefix_is_not.any()),
                             Requires(PrefixIsIn(weakref, self.rules.required_prefix.get()),
                                      is_requirement_active=self.rules.required_prefix.any()),
                             RequiresOrForbids(IsSentenceStart(weakref), self.requires_forbids.sentence_start),
                             RequiresOrForbids(HasTeFormStem(weakref), self.requires_forbids.te_form_stem),
                             RequiresOrForbids(HasAStem(weakref), self.requires_forbids.a_stem),
                             RequiresOrForbids(HasPastTenseStem(weakref), self.requires_forbids.past_tense_stem),
                             RequiresOrForbids(HasEStem(weakref), self.requires_forbids.e_stem),

                             # tail requirements
                             RequiresOrForbids(IsSentenceEnd(weakref), self.requires_forbids.sentence_end),
                             Forbids(SuffixIsIn(weakref, self.rules.suffix_is_not.get()),
                                     is_requirement_active=self.rules.suffix_is_not.any()),

                             # misc requirements
                             Forbids(IsPoisonWord(weakref)),
                             RequiresOrForbids(IsGodanPotential(weakref), self.requires_forbids.godan_potential),
                             RequiresOrForbids(IsGodanImperative(weakref), self.requires_forbids.godan_imperative),
                             RequiresOrForbids(IsExactMatch(weakref), self.requires_forbids.exact_match),
                             RequiresOrForbids(IsSingleToken(weakref), self.requires_forbids.single_token),
                             Forbids(SurfaceIsIn(weakref, self.rules.surface_is_not.get()),
                                     is_requirement_active=self.rules.surface_is_not.any()),
                             Forbids(SurfaceIsIn(weakref, self.rules.yield_to_surface.get()),
                                     is_requirement_active=self.rules.yield_to_surface.any()),
                         ],
                         display_requirements=[
                             Forbids(HasDisplayedOverlappingFollowingCompound(weakref),
                                     is_requirement_active=self.requires_forbids.yield_last_token.is_required)
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
        if self.matching_configuration.bool_flags.question_overrides_form.is_set():
            if self.requires_forbids.a_stem.is_required or self.requires_forbids.e_stem.is_required:
                return super().start_index - 1
            if self.rules.required_prefix.any():
                matched_prefixes = [prefix for prefix in self.rules.required_prefix.get()
                                    if self.parsed_form.startswith(prefix)]
                if matched_prefixes:
                    matched_prefix_length = max(len(prefix) for prefix in matched_prefixes)
                    return super().start_index - matched_prefix_length

        return super().start_index

    @override
    def __repr__(self) -> str: return f"""{self.vocab.get_question()}, {self.vocab.get_answer()[:10]}: {self.match_form[:10]}: failure_reasons: {" ".join(self.failure_reasons) or "None"} ## hiding_reasons: {" ".join(self.hiding_reasons) or "None"}"""
