from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.vocabulary.related_vocab.related_vocab_data_serializer import RelatedVocabDataSerializer

if TYPE_CHECKING:
    from note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper


class RelatedVocabData(Slots):
    serializer: RelatedVocabDataSerializer = RelatedVocabDataSerializer()
    def __init__(self, ergative_twin: str, derived_from: ValueWrapper[str], similar: set[str], antonyms: set[str], confused_with: set[str]) -> None:
        self.ergative_twin: str = ergative_twin
        self.derived_from: ValueWrapper[str] = derived_from

        self.synonyms: set[str] = similar
        self.antonyms: set[str] = antonyms
        self.confused_with: set[str] = confused_with
