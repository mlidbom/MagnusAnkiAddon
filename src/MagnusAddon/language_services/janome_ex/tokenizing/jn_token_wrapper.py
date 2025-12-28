from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.tokenizing.pre_processing_stage.godan_imperative_splitter import GodanImperativeSplitter
from language_services.janome_ex.tokenizing.pre_processing_stage.ichidan_godan_potential_or_imperative_hybrid_splitter import IchidanGodanPotentialOrImperativeHybridSplitter
from language_services.janome_ex.tokenizing.pre_processing_stage.ichidan_imperative_splitter import IchidanImperativeSplitter
from language_services.janome_ex.tokenizing.processed_token import ProcessedToken

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_token import JNToken
    from note.collection.vocab_collection import VocabCollection

class JNTokenWrapper(ProcessedToken, Slots):
    def __init__(self, token: JNToken, vocabs: VocabCollection) -> None:
        super().__init__(token.surface, token.base_form, token.parts_of_speech.is_non_word_character())
        self.token: JNToken = token
        self._vocabs: VocabCollection = vocabs
        self.is_inflectable_word: bool = self.token.is_inflectable_word()

    @override
    def is_past_tense_stem(self) -> bool: return self.token.is_past_tense_stem()
    @override
    def is_te_form_stem(self) -> bool: return self.token.is_te_form_stem()
    @override
    def is_ichidan_masu_stem(self) -> bool: return self.token.is_ichidan_masu_stem()
    @override
    def is_past_tense_marker(self) -> bool: return self.token.is_past_tense_marker()
    @override
    def is_special_nai_negative(self) -> bool: return self.token.is_special_nai_negative()

    def pre_process(self) -> list[ProcessedToken]:  # note: The order here matters, it's not random. any change will break things even should the tests be incomplete and not show it.
        split_godan_imperative = GodanImperativeSplitter(self.token).try_split()
        if split_godan_imperative is not None:
            return split_godan_imperative

        split_godan_imperative = IchidanGodanPotentialOrImperativeHybridSplitter(self.token, self._vocabs).try_split()
        if split_godan_imperative is not None:
            return split_godan_imperative

        split_ichidan_imperative = IchidanImperativeSplitter(self.token).try_split()
        if split_ichidan_imperative is not None:
            return split_ichidan_imperative

        return [self]

