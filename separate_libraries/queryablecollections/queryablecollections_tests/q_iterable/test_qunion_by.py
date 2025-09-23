from __future__ import annotations

from test_common_helpers import lists_value_test


def get_id(item: tuple[int, str]) -> int: return item[0]

def test_combines_unique_items_from_both_sequences_by_id_retaining_the_order_from_both_sequences_keeping_the_first_encountered_duplicate() -> None:
    lists_value_test(
            [(1, "apple"), (2, "banana"), (3, "cherry")],
            lambda x: x.qunion_by([(1, "avocado"), (4, "blueberry"), (5, "apricot")], get_id).to_list(),  # ID 1 conflicts with "apple"
            [(1, "apple"), (2, "banana"), (3, "cherry"), (4, "blueberry"), (5, "apricot")]
    )

def test_removes_duplicates_within_first_sequence() -> None:
    lists_value_test(
            [(1, "apple"), (1, "apricot"), (2, "banana")],
            lambda x: x.qunion_by([(3, "cherry"), (4, "date")], get_id).to_list(),
            [(1, "apple"), (2, "banana"), (3, "cherry"), (4, "date")]
    )

def test_removes_duplicates_within_second_sequence() -> None:
    lists_value_test(
            [(1, "apple"), (2, "banana")],
            lambda x: x.qunion_by([(3, "cherry"), (3, "coconut"), (4, "date")], get_id).to_list(),
            [(1, "apple"), (2, "banana"), (3, "cherry"), (4, "date")]
    )

def test_second_sequence_items_excluded_when_ids_already_exist() -> None:
    lists_value_test(
            [(1, "apple"), (2, "banana"), (3, "cherry")],
            lambda x: x.qunion_by([(1, "avocado"), (2, "blueberry"), (3, "coconut")], get_id).to_list(),
            [(1, "apple"), (2, "banana"), (3, "cherry")]
    )

def test_empty_first_sequence_returns_deduplicated_second_sequence() -> None:
    lists_value_test(
            [],
            lambda x: x.qunion_by([(1, "apple"), (1, "apricot"), (2, "banana")], get_id).to_list(),
            [(1, "apple"), (2, "banana")]
    )

def test_empty_second_sequence_returns_deduplicated_first_sequence() -> None:
    lists_value_test(
            [(1, "apple"), (1, "apricot"), (2, "banana")],
            lambda x: x.qunion_by([], get_id).to_list(),
            [(1, "apple"), (2, "banana")]
    )

def test_both_sequences_empty_returns_empty() -> None:
    lists_value_test(
            [],
            lambda x: x.qunion_by([], lambda item: item).to_list(),
            list[int]())

def test_preserves_order_first_sequence_then_second() -> None:
    lists_value_test(
            [(10, "zebra"), (1, "apple"), (5, "mango")],
            lambda x: x.qunion_by([(7, "elderberry"), (2, "banana"), (1, "apricot")], get_id).to_list(),
            [(10, "zebra"), (1, "apple"), (5, "mango"), (7, "elderberry"), (2, "banana")]
    )

def test_handles_none_ids_correctly() -> None:
    lists_value_test(
            [(None, "unknown1"), (1, "apple"), (2, "banana")],
            lambda x: x.qunion_by([(None, "unknown2"), (3, "cherry"), (4, "date")], lambda item: item[0]).to_list(),
            [(None, "unknown1"), (1, "apple"), (2, "banana"), (3, "cherry"), (4, "date")]
    )

def test_identical_sequences_removes_duplicates() -> None:
    lists_value_test(
            [(1, "apple"), (1, "apricot"), (2, "banana")],
            lambda x: x.qunion_by([(1, "apple"), (1, "apricot"), (2, "banana")], get_id).to_list(),
            [(1, "apple"), (2, "banana")]
    )

def test_completely_different_ids_includes_all_items() -> None:
    lists_value_test(
            [(1, "apple"), (2, "banana"), (3, "cherry")],
            lambda x: x.qunion_by([(4, "date"), (5, "elderberry"), (6, "fig")], get_id).to_list(),
            [(1, "apple"), (2, "banana"), (3, "cherry"), (4, "date"), (5, "elderberry"), (6, "fig")]
    )

def test_single_element_sequences() -> None:
    lists_value_test(
            [(1, "apple")],
            lambda x: x.qunion_by([(2, "banana")], get_id).to_list(),
            [(1, "apple"), (2, "banana")]
    )

def test_single_elements_with_duplicate_ids() -> None:
    lists_value_test(
            [(1, "apple")],
            lambda x: x.qunion_by([(1, "avocado")], get_id).to_list(),
            [(1, "apple")]
    )

def test_numeric_items_with_identity_key() -> None:
    lists_value_test(
            [1, 2, 3],
            lambda x: x.qunion_by([1, 4, 5], lambda item: item).to_list(),
            [1, 2, 3, 4, 5]
    )
