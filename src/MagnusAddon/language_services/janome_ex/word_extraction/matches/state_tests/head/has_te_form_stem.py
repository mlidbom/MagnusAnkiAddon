from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsHasTeFormStem(CustomRequiresOrForbids, Slots):
    _te_forms: QSet[str] = QSet(("て", "って", "で"))
    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector)

    @property
    @override
    def is_required(self) -> bool:
        return self.inspector.match.requires_forbids.te_form_stem.is_required

    @property
    @override
    def is_forbidden(self) -> bool:
        return self.inspector.match.requires_forbids.te_form_stem.is_forbidden

    @property
    @override
    def description(self) -> str: return "te_form_stem"

    @override
    def _internal_is_in_state(self) -> bool:
        #todo get this stuff moved into the tokenizing stage...
        if self.inspector.previous_location is None:
            return False

        if self.inspector.previous_location.token.is_special_nai_negative():  # todo: review: this code means that we do not consider ない to be a te form stem, but it seems that janome does.....
            return False

        if self.inspector.previous_location.token.is_te_form_stem():
            return True

        if not any(te_form_start for te_form_start in RequiresOrForbidsHasTeFormStem._te_forms if self.inspector.parsed_form.startswith(te_form_start)):
            return False

        if self.inspector.previous_location.token.is_past_tense_stem():
            return True

        if self.inspector.previous_location.token.is_ichidan_masu_stem():  # noqa: SIM103
            return True

        return False
