from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class HasTeFormStem(MatchStateTest):
    _te_forms: set[str] = {"て", "って", "で"}
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, "te_form_stem")

    @property
    @override
    def match_is_in_state(self) -> bool:
        #todo get this stuff moved into the tokenizing stage...
        if self.previous_location is None:
            return False

        if self.previous_location.token.is_special_nai_negative():  # todo: review: this code means that we do not consider ない to be a te form stem, but it seems that janome does.....
            return False

        if self.previous_location.token.is_te_form_stem():
            return True

        if not any(te_form_start for te_form_start in HasTeFormStem._te_forms if self.parsed_form.startswith(te_form_start)):
            return False

        if self.previous_location.token.is_past_tense_stem():
            return True

        if self.previous_location.token.is_ichidan_masu_stem():  # noqa: SIM103
            return True

        return False
