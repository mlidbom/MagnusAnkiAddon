from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

class MiscRequirements(Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        vocab = match().vocab
        self.rules = vocab.matching_rules
        self.match = match

        self.is_poison_word = self.rules.is_poison_word.is_set()

        self.is_exact_match_requirement_fulfilled = (not self.rules.requires_exact_match.is_set()
                                                     or (match().word_variant().is_surface and match().word_variant().form in vocab.forms.all_set()))

        self.is_single_token_requirement_fulfilled = (not self.rules.single_token.is_required
                                                      or not match().word_variant().word.is_custom_compound)

        self.is_compound_requirement_fulfilled = (not self.rules.single_token.is_forbidden
                                                  or match().word_variant().word.is_custom_compound)

        surface_is_not = self.rules.rules.surface_is_not.get()
        self.surface_is_not_requirement_fulfilled = (not any(surface_is_not)
                                                     or match().word_variant().is_surface
                                                     or match().word_variant().word.surface_variant.form not in surface_is_not)

        # todo: this should be in display requirements but due to the messed up way we intermingle logic for validity and display that breaks the display. For now we have it here.
        yield_to_surface = self.rules.rules.yield_to_surface.get()
        self.yield_to_surface_requirement_fulfilled = (not any(yield_to_surface)
                                                       or match().word_variant().is_surface
                                                       or match().word_variant().word.surface_variant.form not in yield_to_surface)

        self.are_fulfilled = (self.is_exact_match_requirement_fulfilled
                              and self.is_single_token_requirement_fulfilled
                              and self.surface_is_not_requirement_fulfilled
                              and self.yield_to_surface_requirement_fulfilled
                              and self.is_compound_requirement_fulfilled
                              and not self.is_poison_word)

    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(not self.is_exact_match_requirement_fulfilled, "requires_exact_match")
                .append_if(not self.is_single_token_requirement_fulfilled, "requires_single_token")
                .append_if(not self.yield_to_surface_requirement_fulfilled, f"yield_to_surface_{self.match().word_variant().word.surface_variant.form}")
                .append_if(not self.is_compound_requirement_fulfilled, "requires_compound")
                .append_if(not self.surface_is_not_requirement_fulfilled, f"surface_is_not_{self.match().word_variant().word.surface_variant.form}")
                .append_if(self.is_poison_word, "is_poison_word")
                .as_set())

    def __repr__(self) -> str: return " ".join(self.failure_reasons())
