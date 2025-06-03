from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services import conjugator
from sysutils import kana_utils
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class StemRequirements(Slots):
    def __init__(self, vocab: VocabNote, end_of_stem: WeakRef[TextAnalysisLocation] | None) -> None:
        rules = vocab.matching_rules
        self.config = rules
        self.are_fulfilled = True

        self.are_fulfilled = True
        self.fulfills_forbids_a_stem_requirement = not rules.forbids_a_stem.is_set() or (end_of_stem is None or end_of_stem().token.surface[-1] not in conjugator.a_stem_characters)
        self.fulfills_requires_a_stem = not rules.requires_a_stem.is_set() or (end_of_stem is not None and end_of_stem().token.surface[-1] in conjugator.a_stem_characters)
        self.fulfills_requires_e_stem_requirement = not rules.requires_e_stem.is_set() or (end_of_stem is not None
                                                                                           and (end_of_stem().token.surface[-1] in conjugator.e_stem_characters
                                                                                                or kana_utils.character_is_kanji(end_of_stem().token.surface[-1])))

        self.are_fulfilled = (self.are_fulfilled
                              and self.fulfills_forbids_a_stem_requirement
                              and self.fulfills_requires_a_stem
                              and self.fulfills_requires_e_stem_requirement)

    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if("fails_forbids_a_stem_requirement", not self.fulfills_forbids_a_stem_requirement)
                .append_if("fails_requires_a_stem", not self.fulfills_requires_a_stem)
                .append_if("fails_requires_e_stem_requirement", not self.fulfills_requires_e_stem_requirement)
                .as_set())

    def __repr__(self) -> str: return " ".join(self.failure_reasons())