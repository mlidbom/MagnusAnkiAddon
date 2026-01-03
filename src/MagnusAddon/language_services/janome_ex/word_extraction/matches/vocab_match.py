from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from configuration.configuration_cache_impl import ConfigurationCache
from language_services.janome_ex.word_extraction.matches.match import Match
from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
from language_services.janome_ex.word_extraction.matches.state_tests.another_match_owns_the_form import ForbidsAnotherMatchOwnsTheForm
from language_services.janome_ex.word_extraction.matches.state_tests.forbids_compositionally_transparent_compound import ForbidsCompositionallyTransparentCompound
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_a_stem import RequiresOrForbidsHasAStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_e_stem import RequiresOrForbidsHasEStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_godan_imperative_prefix import RequiresOrForbidsHasGodanImperativePrefix
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_past_tense_stem import RequiresOrForbidsHasPastTenseStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_te_form_stem import RequiresOrForbidsHasTeFormStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.is_sentence_start import RequiresOrForbidsIsSentenceStart
from language_services.janome_ex.word_extraction.matches.state_tests.head.prefix_is_in import ForbidsPrefixIsIn, RequiresPrefixIsIn
from language_services.janome_ex.word_extraction.matches.state_tests.is_exact_match import RequiresOrForbidsIsExactMatch
from language_services.janome_ex.word_extraction.matches.state_tests.is_ichidan_imperative import RequiresOrForbidsStartsWithIchidanImperativeStemOrInflection
from language_services.janome_ex.word_extraction.matches.state_tests.is_poison_word import ForbidsIsPoisonWord
from language_services.janome_ex.word_extraction.matches.state_tests.is_single_token import RequiresOrForbidsIsSingleToken
from language_services.janome_ex.word_extraction.matches.state_tests.starts_with_godan_imperative_stem_or_inflection import RequiresOrForbidsStartsWithGodanImperativeStemOrInflection
from language_services.janome_ex.word_extraction.matches.state_tests.starts_with_godan_potential_stem_or_inflection import RequiresOrForbidsStartsWithGodanPotentialStemOrInflection
from language_services.janome_ex.word_extraction.matches.state_tests.surface_is_in import ForbidsSurfaceIsIn
from language_services.janome_ex.word_extraction.matches.state_tests.tail.has_overlapping_following_compound import ForbidsHasDisplayedOverlappingFollowingCompound
from language_services.janome_ex.word_extraction.matches.state_tests.tail.is_sentence_end import RequiresOrForbidsIsSentenceEnd
from language_services.janome_ex.word_extraction.matches.state_tests.tail.suffix_is_in import ForbidsSuffixIsIn
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote import VocabNote
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration

@final
class VocabMatch(Match, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], vocab: VocabNote) -> None:
        weakref: WeakRef[VocabMatch] = WeakRef(self)
        inspector = VocabMatchInspector(weakref)
        self.requires_forbids = vocab.matching_configuration.requires_forbids
        self.rules = vocab.matching_configuration.configurable_rules
        super().__init__(word_variant,
                         validity_requirements=(
                                 ForbidsAnotherMatchOwnsTheForm(inspector),
                                 # head requirements
                                 ForbidsPrefixIsIn.for_if(inspector, self.rules.prefix_is_not.get()),
                                 RequiresPrefixIsIn.for_if(inspector, self.rules.required_prefix.get()),
                                 RequiresOrForbidsIsSentenceStart.for_if(inspector),
                                 RequiresOrForbidsHasTeFormStem.for_if(inspector),
                                 RequiresOrForbidsHasAStem.for_if(inspector),
                                 RequiresOrForbidsHasPastTenseStem.for_if(inspector),
                                 RequiresOrForbidsHasEStem.for_if(inspector),

                                 RequiresOrForbidsHasGodanImperativePrefix.for_if(inspector),
                                 RequiresOrForbidsStartsWithGodanPotentialStemOrInflection.for_if(inspector),
                                 RequiresOrForbidsStartsWithGodanImperativeStemOrInflection.for_if(inspector),
                                 RequiresOrForbidsStartsWithIchidanImperativeStemOrInflection.for_if(inspector),

                                 # tail requirements
                                 RequiresOrForbidsIsSentenceEnd.for_if(inspector),
                                 ForbidsSuffixIsIn.for_if(inspector, self.rules.suffix_is_not.get()),

                                 # misc requirements
                                 ForbidsIsPoisonWord(inspector),

                                 RequiresOrForbidsIsExactMatch.for_if(inspector),
                                 RequiresOrForbidsIsSingleToken.for_if(inspector),
                                 ForbidsSurfaceIsIn.for_if(inspector, self.rules.surface_is_not.get()),
                                 ForbidsSurfaceIsIn.for_if(inspector, self.rules.yield_to_surface.get()),
                         ),
                         display_requirements=(
                                 ForbidsHasDisplayedOverlappingFollowingCompound.for_if(inspector, self.requires_forbids.yield_last_token.is_required),
                                 ForbidsCompositionallyTransparentCompound.for_if(ConfigurationCache.hide_transparent_compounds() and vocab.matching_configuration.bool_flags.is_compositionally_transparent_compound.is_set())
                         ))
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

    @override
    def _start_index(self) -> int:
        if self.matching_configuration.bool_flags.question_overrides_form.is_set():
            length_diff = (len(self.vocab.get_question()) - len(self.tokenized_form))
            if length_diff != 0 and self.tokenized_form in self.vocab.get_question():  # we often "steal" characters backwards, forwards is not supported so this should be sufficient, we don't need all the complexity below
                return super()._start_index() - length_diff
            if self.requires_forbids.a_stem.is_required or self.requires_forbids.e_stem.is_required:
                return super()._start_index() - 1
            if self.rules.required_prefix.any():
                matched_prefixes = [prefix for prefix in self.rules.required_prefix.get()
                                    if self.parsed_form.startswith(prefix)]
                if matched_prefixes:
                    matched_prefix_length = max(len(prefix) for prefix in matched_prefixes)
                    return super()._start_index() - matched_prefix_length

        return super()._start_index()

    @override
    def __repr__(self) -> str: return f"""{self.vocab.get_question()}, {self.vocab.get_answer()[:10]}: {self.match_form[:10]}: failure_reasons: {" ".join(self.failure_reasons) or "None"} ## hiding_reasons: {" ".join(self.hiding_reasons) or "None"}"""
