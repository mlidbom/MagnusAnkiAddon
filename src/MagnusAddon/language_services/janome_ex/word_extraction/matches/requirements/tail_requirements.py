from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.analysis_constants import non_word_characters
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

_quote_characters = {"と", "って"}

class TailRequirements(Slots):
    def __init__(self, vocab: VocabNote, tail: WeakRef[TextAnalysisLocation] | None) -> None:
        self.config = vocab.matching_rules
        rules = vocab.matching_rules

        self.has_suffix = tail is not None and tail().token.surface != "" and tail().token.surface[-1] not in non_word_characters

        self.fulfills_requires_sentence_end_requirement = (not self.config.sentence_end.is_required
                                                           or (tail is None or tail().token.is_non_word_character or tail().token.surface in _quote_characters))

        self.fulfills_forbids_sentence_end_requirement = (not self.config.sentence_end.is_forbidden
                                                          or (tail is not None and not tail().token.is_non_word_character and tail().token.surface not in _quote_characters))

        self.fulfills_suffix_is_not = (not rules.rules.suffix_is_not.get()
                                       or not self.has_suffix
                                       or (tail is not None and not any(forbidden for forbidden in rules.rules.suffix_is_not.get() if tail().token.surface.startswith(forbidden))))

        self.are_fulfilled = (self.fulfills_requires_sentence_end_requirement
                              and self.fulfills_forbids_sentence_end_requirement
                              and self.fulfills_suffix_is_not)

    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(not self.fulfills_requires_sentence_end_requirement, "requires_sentence_end")
                .append_if(not self.fulfills_forbids_sentence_end_requirement, "forbids_sentence_end")
                .append_if(not self.fulfills_suffix_is_not, "suffix_is_not")
                .as_set())

    def __repr__(self) -> str: return " ".join(self.failure_reasons())
