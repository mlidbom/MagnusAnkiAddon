from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

@final
class TailRequirements(Slots):
    def __init__(self, vocab: VocabNote, tail: WeakRef[TextAnalysisLocation] | None) -> None:
        self.config = vocab.matching_configuration
        rules = vocab.matching_configuration

        self.has_suffix: bool = tail is not None and tail().token.surface != "" and not tail().token.surface[-1].isspace()

        self.fulfills_suffix_is_not: bool = (not rules.configurable_rules.suffix_is_not.get()
                                             or not self.has_suffix
                                             or (tail is not None and not any(forbidden for forbidden in rules.configurable_rules.suffix_is_not.get() if tail().token.surface.startswith(forbidden))))

        self.are_fulfilled: bool =  self.fulfills_suffix_is_not

    def failure_reasons(self) -> list[str]:
        return (SimpleStringListBuilder()
                .append_if(not self.fulfills_suffix_is_not, "suffix_is_not")
                .value)

    @override
    def __repr__(self) -> str: return " ".join(self.failure_reasons())
