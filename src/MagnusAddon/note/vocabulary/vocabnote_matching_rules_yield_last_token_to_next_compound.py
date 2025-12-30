from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.notefields.require_forbid_flag_field import RequireForbidFlagField
from note.tags import Tags
from sysutils.simple_string_builder import SimpleStringBuilder
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from configuration.configuration_value import ConfigurationValueBool
    from note.vocabulary.vocabnote import VocabNote
    from note.vocabulary.vocabnote_parts_of_speech import VocabNotePartsOfSpeech

class YieldLastTokenToOverlappingCompound(RequireForbidFlagField, WeakRefable, Slots):
    automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound: ConfigurationValueBool = app.config().automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound
    automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound: ConfigurationValueBool = app.config().automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound
    automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound: ConfigurationValueBool = app.config().automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound

    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        super().__init__(vocab, Tags.Vocab.Matching.yield_last_token_to_overlapping_compound, Tags.Vocab.Matching.Forbids.auto_yielding)

    @property
    def _vocab(self) -> VocabNote: return cast("VocabNote", self._note())

    @property
    def _pos(self) -> VocabNotePartsOfSpeech: return self._vocab.parts_of_speech

    def _decide_if_required(self) -> bool:
        return (super().is_required
                or (not self.is_forbidden
                    and (  # na adjectives
                            self._pos.is_complete_na_adjective()
                            # suru verb compounds
                            or (self.automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound.get_value()
                                and self._pos.is_suru_verb_included()
                                and not self._pos.is_ni_suru_ga_suru_ku_suru_compound())
                            # passive verb compounds
                            or (self.automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound.get_value()
                                and self._pos.is_passive_verb_compound())
                            # causative verb compounds
                            or (self.automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound.get_value()
                                and self._pos.is_causative_verb_compound())
                    )))

    @property
    @override
    def is_required(self) -> bool: return self._decide_if_required()

    @override
    def __repr__(self) -> str: return (SimpleStringBuilder()
                                       .append_if(self.is_required, "required")
                                       .append_if(self.is_forbidden, "forbidden")
                                       .build())
