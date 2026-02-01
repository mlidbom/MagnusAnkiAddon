from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.sysutils.lazy import Lazy
from jastudio.note.vocabulary.related_vocab.related_vocab_data_serializer import RelatedVocabDataSerializer

if TYPE_CHECKING:
    from jastudio.note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper
    from typed_linq_collections.collections.q_set import QSet

class RelatedVocabData(Slots):
    serializer: Lazy[RelatedVocabDataSerializer] = Lazy(RelatedVocabDataSerializer)

    def __init__(self, ergative_twin: str, derived_from: ValueWrapper[str], perfect_synonyms: QSet[str], similar: QSet[str], antonyms: QSet[str], confused_with: QSet[str], see_also: QSet[str]) -> None:
        self.ergative_twin: str = ergative_twin
        self.derived_from: ValueWrapper[str] = derived_from

        self.synonyms: QSet[str] = similar
        self.perfect_synonyms: QSet[str] = perfect_synonyms
        self.antonyms: QSet[str] = antonyms
        self.confused_with: QSet[str] = confused_with
        self.see_also: QSet[str] = see_also

    @override
    def __repr__(self) -> str: return f"RelatedVocabData(ergative_twin={self.ergative_twin}, derived_from={self.derived_from}, perfect_synonyms={self.perfect_synonyms}, synonyms={self.synonyms}, antonyms={self.antonyms}, confused_with={self.confused_with}, see_also={self.see_also})"
