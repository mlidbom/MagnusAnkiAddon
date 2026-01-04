from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.tokenizing.jn_token_wrapper import JNTokenWrapper
from language_services.janome_ex.tokenizing.pre_processing_stage.godan_imperative_splitter import GodanImperativeSplitter
from language_services.janome_ex.tokenizing.pre_processing_stage.ichidan_godan_potential_or_imperative_hybrid_splitter import IchidanGodanPotentialOrImperativeHybridSplitter
from language_services.janome_ex.tokenizing.pre_processing_stage.ichidan_imperative_splitter import IchidanImperativeSplitter

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_token import JNToken
    from language_services.janome_ex.tokenizing.processed_token import ProcessedToken
    from note.collection.vocab_collection import VocabCollection


class PreProcessingStage(Slots):
    def __init__(self, vocabs: VocabCollection) -> None:
        self._vocabs: VocabCollection = vocabs

    def pre_process(self, tokens: list[JNToken]) -> list[ProcessedToken]:
        return [processed for token in tokens for processed in self.pre_process_token(token)]


    def pre_process_token(self, token: JNToken) -> list[ProcessedToken]:  # note: The order here matters, it's not random. any change will break things even should the tests be incomplete and not show it.
        split_godan_imperative = GodanImperativeSplitter.try_split(token)
        if split_godan_imperative is not None:
            return split_godan_imperative

        split_godan_imperative = IchidanGodanPotentialOrImperativeHybridSplitter(token, self._vocabs).try_split()
        if split_godan_imperative is not None:
            return split_godan_imperative

        split_ichidan_imperative = IchidanImperativeSplitter.try_split(token)
        if split_ichidan_imperative is not None:
            return split_ichidan_imperative

        return [JNTokenWrapper(token, self._vocabs)]