from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots
from note.vocabulary.related_vocab.related_vocab_data_serializer import RelatedVocabDataSerializer

if TYPE_CHECKING:
    from note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper


class RelatedVocabData(ProfilableAutoSlots):
    serializer: RelatedVocabDataSerializer = RelatedVocabDataSerializer()
    def __init__(self, ergative_twin: str, derived_from: ValueWrapper[str], perfect_synonyms: set[str], similar: set[str], antonyms: set[str], confused_with: set[str], see_also:set[str]) -> None:
        self.ergative_twin: str = ergative_twin
        self.derived_from: ValueWrapper[str] = derived_from

        self.synonyms: set[str] = similar
        self.perfect_synonyms: set[str] = perfect_synonyms
        self.antonyms: set[str] = antonyms
        self.confused_with: set[str] = confused_with
        self.see_also:set[str] = see_also

    @override
    def __repr__(self) -> str: return f"RelatedVocabData(ergative_twin={self.ergative_twin}, derived_from={self.derived_from}, perfect_synonyms={self.perfect_synonyms}, synonyms={self.synonyms}, antonyms={self.antonyms}, confused_with={self.confused_with}, see_also={self.see_also})"