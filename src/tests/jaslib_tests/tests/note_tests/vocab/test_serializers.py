from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from jaslib.note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper
from jaslib.note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
from jaslib.note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingRulesData
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from jaslib.note.vocabulary.related_vocab.related_vocab_data_serializer import RelatedVocabDataSerializer
    from jaslib.note.vocabulary.serialization.matching_rules_serializer import VocabNoteMatchingRulesSerializer


class TestRelatedVocabDataSerializer:
    @pytest.fixture
    def serializer(self) -> RelatedVocabDataSerializer:
        return RelatedVocabData.serializer()

    def test_empty_object_serializes_to_empty_string(self, serializer: RelatedVocabDataSerializer) -> None:
        empty_data = RelatedVocabData(
                ergative_twin="",
                derived_from=ValueWrapper(""),
                perfect_synonyms=QSet(),
                similar=QSet(),
                antonyms=QSet(),
                confused_with=QSet(),
                see_also=QSet()
        )

        result = serializer.serialize(empty_data)

        assert result == ""

    def test_deserialize_empty_string_returns_empty_data(self, serializer: RelatedVocabDataSerializer) -> None:
        result = serializer.deserialize("")

        assert result.ergative_twin == ""
        assert result.derived_from.get() == ""
        assert result.perfect_synonyms == QSet()
        assert result.synonyms == QSet()
        assert result.antonyms == QSet()
        assert result.confused_with == QSet()
        assert result.see_also == QSet()

    def test_roundtrip_with_data_preserves_all_fields(self, serializer: RelatedVocabDataSerializer) -> None:
        original = RelatedVocabData(
                ergative_twin="開く",
                derived_from=ValueWrapper("開ける"),
                perfect_synonyms=QSet(["完璧", "完全"]),
                similar=QSet(["似ている", "同様"]),
                antonyms=QSet(["閉じる", "閉める"]),
                confused_with=QSet(["明く"]),
                see_also=QSet(["開放", "開始"])
        )

        serialized = serializer.serialize(original)
        deserialized = serializer.deserialize(serialized)

        assert deserialized.ergative_twin == "開く"
        assert deserialized.derived_from.get() == "開ける"
        assert deserialized.perfect_synonyms == QSet(["完璧", "完全"])
        assert deserialized.synonyms == QSet(["似ている", "同様"])
        assert deserialized.antonyms == QSet(["閉じる", "閉める"])
        assert deserialized.confused_with == QSet(["明く"])
        assert deserialized.see_also == QSet(["開放", "開始"])


class TestVocabNoteMatchingRulesSerializer:
    @pytest.fixture
    def serializer(self) -> VocabNoteMatchingRulesSerializer:
        return VocabNoteMatchingRulesData.serializer()

    def test_empty_object_serializes_to_empty_string(self, serializer: VocabNoteMatchingRulesSerializer) -> None:
        empty_data = VocabNoteMatchingRulesData(
                surface_is_not=QSet(),
                prefix_is_not=QSet(),
                suffix_is_not=QSet(),
                required_prefix=QSet(),
                yield_to_surface=QSet()
        )

        result = serializer.serialize(empty_data)

        assert result == ""

    def test_roundtrip_with_data_preserves_all_fields(self, serializer: VocabNoteMatchingRulesSerializer) -> None:
        original = VocabNoteMatchingRulesData(
                surface_is_not=QSet(["surface1", "surface2"]),
                prefix_is_not=QSet(["prefix1"]),
                suffix_is_not=QSet(["suffix1", "suffix2", "suffix3"]),
                required_prefix=QSet(["req1"]),
                yield_to_surface=QSet(["yield1", "yield2"])
        )

        serialized = serializer.serialize(original)
        deserialized = serializer.deserialize(serialized)

        assert deserialized.surface_is_not == QSet(["surface1", "surface2"])
        assert deserialized.prefix_is_not == QSet(["prefix1"])
        assert deserialized.suffix_is_not == QSet(["suffix1", "suffix2", "suffix3"])
        assert deserialized.required_prefix == QSet(["req1"])
        assert deserialized.yield_to_surface == QSet(["yield1", "yield2"])
