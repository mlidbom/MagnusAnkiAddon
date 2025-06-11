from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from note.note_constants import Tags
from note.notefields.require_forbid_flag_field import RequireForbidFlagField
from sysutils.simple_string_builder import SimpleStringBuilder

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class YieldLastTokenToOverlappingCompound(RequireForbidFlagField):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        super().__init__(vocab, Tags.Vocab.Matching.yield_last_token_to_overlapping_compound, Tags.Vocab.Matching.Forbids.auto_yielding)
        self._vocab: WeakRef[VocabNote] = vocab

    @property
    def is_required(self) -> bool:
        return (super().is_required
                or (not self.is_forbidden
                    and ((app.config().automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound.get_value()
                          and self._vocab().parts_of_speech.is_suru_verb_included()
                          and not self._vocab().parts_of_speech.is_ni_suru_ga_suru_ku_suru_compound())
                         or (app.config().automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound.get_value()
                             and self._vocab().parts_of_speech.is_passive_verb_compound())
                         or (app.config().automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound.get_value()
                             and self._vocab().parts_of_speech.is_causative_verb_compound())
                         )))

    def __repr__(self) -> str: return (SimpleStringBuilder()
                                       .append_if(self.is_required, "required")
                                       .append_if(self.is_forbidden, "forbidden")
                                       .build())
