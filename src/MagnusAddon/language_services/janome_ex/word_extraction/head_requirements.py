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

class HeadRequirements(Slots):
    def __init__(self, vocab: VocabNote, end_of_stem: WeakRef[TextAnalysisLocation] | None) -> None:
        rules = vocab.matching_rules
        self.config = rules

        self.fulfills_requires_prefix = not rules.is_strictly_suffix or end_of_stem is not None

        self.has_a_stem = end_of_stem is not None and end_of_stem().token.surface[-1] in conjugator.a_stem_characters
        self.fulfills_forbids_a_stem_requirement = not rules.a_stem.is_forbidden or not self.has_a_stem
        self.fulfills_requires_a_stem = not rules.a_stem.is_required or self.has_a_stem

        self.has_e_stem = (end_of_stem is not None and
                           (end_of_stem().token.surface[-1] in conjugator.e_stem_characters
                            or kana_utils.character_is_kanji(end_of_stem().token.surface[-1])))

        self.fulfills_requires_e_stem_requirement = not rules.e_stem.is_required or self.has_e_stem
        self.fulfills_forbids_e_stem_requirement = not rules.e_stem.is_forbidden or not self.has_e_stem

        self.are_fulfilled = (self.fulfills_forbids_a_stem_requirement
                              and self.fulfills_requires_a_stem
                              and self.fulfills_requires_e_stem_requirement
                              and self.fulfills_forbids_e_stem_requirement)

    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(not self.fulfills_forbids_a_stem_requirement, "forbids_a_stem")
                .append_if(not self.fulfills_requires_a_stem, "requires_a_stem")
                .append_if(not self.fulfills_forbids_e_stem_requirement, "forbids_e_stem")
                .append_if(not self.fulfills_requires_e_stem_requirement, "requires_e_stem")
                .as_set())

    def __repr__(self) -> str: return " ".join(self.failure_reasons())
