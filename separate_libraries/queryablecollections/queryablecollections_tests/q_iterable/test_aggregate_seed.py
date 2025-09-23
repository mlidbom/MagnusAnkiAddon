from __future__ import annotations

from test_common_helpers import lists_value_test


def test_aggregate_maintains_order() -> None:
    lists_value_test([1, 2, 3, 4],
                     lambda x: x.aggregate(lambda acc, item: [item] + acc, []),
                     [4, 3, 2, 1])

def test_aggregate_seed_sums_with_initial_value() -> None:
    lists_value_test([1, 2, 3, 4, 5],
                     lambda x: x.aggregate(lambda acc, item: acc + item, 10),
                     25)

def test_aggregate_seed_builds_list() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.aggregate(lambda acc, item: acc + [item * 2], list[int]()),
                     [2, 4, 6])

def test_aggregate_seed_counts_elements() -> None:
    lists_value_test(["a", "bb", "ccc"],
                     lambda x: x.aggregate(lambda count, _: count + 1, 0),
                     3)

def test_aggregate_seed_works_with_empty_sequence() -> None:
    lists_value_test(list[str](),
                     lambda x: x.aggregate(lambda acc, item: acc + item, "initial"),
                     "initial")

def test_aggregate_seed_concatenates_with_separator() -> None:
    lists_value_test(["apple", "banana", "cherry"],
                     lambda x: x.aggregate(lambda acc, item: acc + (", " if acc else "") + item, ""),
                     "apple, banana, cherry")
