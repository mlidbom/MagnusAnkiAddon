from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

_quote_characters = {"と", "って"}

class TailRequirements(Slots):
    def __init__(self, vocab: VocabNote, tail: WeakRef[TextAnalysisLocation] | None) -> None:
        self.config = vocab.matching_rules
        self.fulfills_requires_sentence_end_requirement = (not self.config.requires_sentence_end.is_set()
                                                           or (tail is None or tail().token.is_non_word_character or tail().token.surface in _quote_characters))

        self.are_fulfilled = self.fulfills_requires_sentence_end_requirement

    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if("fails_requires_sentence_end_requirement", not self.fulfills_requires_sentence_end_requirement)
                .as_set())

    def __repr__(self) -> str: return " ".join(self.failure_reasons())