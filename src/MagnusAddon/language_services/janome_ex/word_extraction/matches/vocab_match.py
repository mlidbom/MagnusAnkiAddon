from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots
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
from language_services.janome_ex.word_extraction.matches.state_tests.head.requires_forbids_adverb_stem import RequiresOrForbidsPrecedingAdverb
from language_services.janome_ex.word_extraction.matches.state_tests.head.requires_forbids_masu_stem import RequiresOrForbidsMasuStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.requires_or_forbids_dictionary_form_prefix import RequiresOrForbidsDictionaryFormPrefix
from language_services.janome_ex.word_extraction.matches.state_tests.head.requires_or_forbids_dictionary_form_stem import RequiresOrForbidsDictionaryFormStem
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
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from note.vocabulary.vocabnote import VocabNote
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration

@final
class VocabMatch(Match, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], vocab: VocabNote) -> None:
        self.weakref_vocab: WeakRef[VocabMatch] = WeakRef(self)
        self.vocab_inspector = VocabMatchInspector(self.weakref_vocab)
        self.requires_forbids = vocab.matching_configuration.requires_forbids
        self.rules = vocab.matching_configuration.configurable_rules
        self.vocab: VocabNote = vocab
        self._variant: WeakRef[CandidateWordVariant] = word_variant
        self._another_match_owns_the_form_cache: bool | None = None
        super().__init__(word_variant)

    @override
    def _create_display_requirements(self) -> tuple[MatchRequirement | None, ...]:
        return (
                ForbidsHasDisplayedOverlappingFollowingCompound.apply_to(self.vocab_inspector, self.requires_forbids.yield_last_token.is_required),
                ForbidsCompositionallyTransparentCompound.apply_to(self.vocab_inspector)
        )

    @override
    def _create_primary_validity_requirements(self) -> tuple[MatchRequirement | None, ...]:
        return (
                # head requirements
                ForbidsPrefixIsIn.apply_to(self.vocab_inspector, self.rules.prefix_is_not.get()),
                RequiresPrefixIsIn.apply_to(self.vocab_inspector, self.rules.required_prefix.get()),
                RequiresOrForbidsIsSentenceStart.apply_to(self.vocab_inspector),
                RequiresOrForbidsHasTeFormStem.apply_to(self.vocab_inspector),
                RequiresOrForbidsHasAStem.apply_to(self.vocab_inspector),
                RequiresOrForbidsHasPastTenseStem.apply_to(self.vocab_inspector),
                RequiresOrForbidsHasEStem.apply_to(self.vocab_inspector),

                RequiresOrForbidsHasGodanImperativePrefix.apply_to(self.vocab_inspector),
                RequiresOrForbidsStartsWithGodanPotentialStemOrInflection.apply_to(self.vocab_inspector),
                RequiresOrForbidsStartsWithGodanImperativeStemOrInflection.apply_to(self.vocab_inspector),
                RequiresOrForbidsStartsWithIchidanImperativeStemOrInflection.apply_to(self.vocab_inspector),

                # tail requirements
                RequiresOrForbidsIsSentenceEnd.apply_to(self.vocab_inspector),
                ForbidsSuffixIsIn.apply_to(self.vocab_inspector, self.rules.suffix_is_not.get()),

                # misc requirements
                ForbidsIsPoisonWord.apply_to(self.vocab_inspector),
                RequiresOrForbidsMasuStem.apply_to(self.vocab_inspector),
                RequiresOrForbidsPrecedingAdverb.apply_to(self.vocab_inspector),
                RequiresOrForbidsDictionaryFormStem.apply_to(self.vocab_inspector),
                RequiresOrForbidsDictionaryFormPrefix.apply_to(self.vocab_inspector),

                RequiresOrForbidsIsExactMatch.apply_to(self.vocab_inspector),
                RequiresOrForbidsIsSingleToken.apply_to(self.vocab_inspector),
                ForbidsSurfaceIsIn.apply_to(self.vocab_inspector, self.rules.surface_is_not.get()),
                ForbidsSurfaceIsIn.apply_to(self.vocab_inspector, self.rules.yield_to_surface.get()),  # todo this should be in display requirements right?
        )

    @override
    def _create_interdependent_validity_requirements(self) -> tuple[MatchRequirement | None, ...]:
        return ForbidsAnotherMatchOwnsTheForm.apply_to(self.vocab_inspector),

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
    def _is_valid(self) -> bool:
        return (self._is_valid_internal
                or (self.is_highlighted
                    and not any(match for match in self.variant.vocab_matches if match != self and match._is_valid_internal)))  # We never mix vocab matches with other matches so using the vocab specific collection is fine

    @property
    def another_match_is_higher_priority(self) -> bool:
        if self._another_match_owns_the_form_cache is None:
            if any(other_match for other_match in self.variant.vocab_matches  # noqa: SIM103
                   if other_match != self
                      and other_match.is_primarily_valid
                      and other_match._is_higher_priority_for_match(self)):
                self._another_match_owns_the_form_cache = True
            else:
                self._another_match_owns_the_form_cache = False

        return self._another_match_owns_the_form_cache

    def _is_higher_priority_for_match(self, other: VocabMatch) -> bool:
        if self.vocab.forms.is_owned_form(self.tokenized_form) and not other.vocab.forms.is_owned_form(self.tokenized_form):  # noqa: SIM103
            return True
        if self.vocab.matching_configuration.has_custom_requirements and not other.matching_configuration.has_custom_requirements:  # noqa: SIM103
            return True
        return False

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
