from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from note.notefields.auto_save_wrappers.value_wrapper import ValueWrapper
from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingRulesData
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from note.vocabulary.related_vocab.related_vocab_data_serializer import RelatedVocabDataSerializer
    from note.vocabulary.serialization.matching_rules_serializer import VocabNoteMatchingRulesSerializer


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

    def test_non_empty_data_does_not_serialize_to_empty_string(self, serializer: RelatedVocabDataSerializer) -> None:
        # Test with just one field populated
        data_with_ergative = RelatedVocabData(
                ergative_twin="開く",
                derived_from=ValueWrapper(""),
                perfect_synonyms=QSet(),
                similar=QSet(),
                antonyms=QSet(),
                confused_with=QSet(),
                see_also=QSet()
        )
        assert serializer.serialize(data_with_ergative) != ""

        data_with_derived = RelatedVocabData(
                ergative_twin="",
                derived_from=ValueWrapper("base"),
                perfect_synonyms=QSet(),
                similar=QSet(),
                antonyms=QSet(),
                confused_with=QSet(),
                see_also=QSet()
        )
        assert serializer.serialize(data_with_derived) != ""

        data_with_synonyms = RelatedVocabData(
                ergative_twin="",
                derived_from=ValueWrapper(""),
                perfect_synonyms=QSet(),
                similar=QSet(["synonym"]),
                antonyms=QSet(),
                confused_with=QSet(),
                see_also=QSet()
        )
        assert serializer.serialize(data_with_synonyms) != ""

    def test_multiple_roundtrips_are_stable(self, serializer: RelatedVocabDataSerializer) -> None:
        """Ensure serializing and deserializing multiple times produces identical results."""
        original = RelatedVocabData(
                ergative_twin="test",
                derived_from=ValueWrapper("source"),
                perfect_synonyms=QSet(["a", "b"]),
                similar=QSet(["c"]),
                antonyms=QSet(["d"]),
                confused_with=QSet(["e"]),
                see_also=QSet(["f"])
        )

        first_serialized = serializer.serialize(original)
        first_deserialized = serializer.deserialize(first_serialized)
        second_serialized = serializer.serialize(first_deserialized)

        assert first_serialized == second_serialized

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

    def test_multiple_roundtrips_are_stable(self, serializer: VocabNoteMatchingRulesSerializer) -> None:
        """Ensure serializing and deserializing multiple times produces identical results."""
        original = VocabNoteMatchingRulesData(
                surface_is_not=QSet(["a", "b"]),
                prefix_is_not=QSet(["c"]),
                suffix_is_not=QSet(["d"]),
                required_prefix=QSet(["e"]),
                yield_to_surface=QSet(["f"])
        )

        first_serialized = serializer.serialize(original)
        first_deserialized = serializer.deserialize(first_serialized)
        second_serialized = serializer.serialize(first_deserialized)

        assert first_serialized == second_serialized
