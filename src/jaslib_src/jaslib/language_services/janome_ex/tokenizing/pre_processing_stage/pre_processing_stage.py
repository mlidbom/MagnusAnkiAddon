from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

from jaslib.language_services.janome_ex.tokenizing.jn_token import JNToken
from jaslib.language_services.janome_ex.tokenizing.pre_processing_stage.dictionary_form_verb_splitter import DictionaryFormVerbSplitter
from jaslib.language_services.janome_ex.tokenizing.pre_processing_stage.godan_imperative_splitter import GodanImperativeSplitter
from jaslib.language_services.janome_ex.tokenizing.pre_processing_stage.ichidan_godan_potential_or_imperative_hybrid_splitter import IchidanGodanPotentialOrImperativeHybridSplitter
from jaslib.language_services.janome_ex.tokenizing.pre_processing_stage.ichidan_imperative_splitter import IchidanImperativeSplitter

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
    from jaslib.note.collection.vocab_collection import VocabCollection

class PreProcessingStage(Slots):
    def __init__(self, vocabs: VocabCollection) -> None:
        self._vocabs: VocabCollection = vocabs

    def pre_process(self, tokens: list[JNToken]) -> list[IAnalysisToken]:
        return [processed for token in tokens for processed in self.pre_process_token(token)]

    def pre_process_token(self, token: JNToken) -> list[IAnalysisToken]:  # note: The order here matters, it's not random. any change will break things even should the tests be incomplete and not show it.
        if token.surface == JNToken.SPLITTER_TOKEN_TEXT:
            return []

        split_godan_imperative = GodanImperativeSplitter.try_split(token)
        if split_godan_imperative is not None:
            return split_godan_imperative

        split_godan_imperative = IchidanGodanPotentialOrImperativeHybridSplitter.try_split(token, self._vocabs)
        if split_godan_imperative is not None:
            return split_godan_imperative

        split_ichidan_imperative = IchidanImperativeSplitter.try_split(token)
        if split_ichidan_imperative is not None:
            return split_ichidan_imperative

        split_dictionary_form_verb = DictionaryFormVerbSplitter.try_split(token)
        if split_dictionary_form_verb is not None:
            return split_dictionary_form_verb

        return [token]
