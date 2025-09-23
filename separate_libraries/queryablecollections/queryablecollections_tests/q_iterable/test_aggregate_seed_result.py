from __future__ import annotations

from test_common_helpers import lists_value_test


def test_aggregate_seed_result_sums_and_formats() -> None:
    lists_value_test([1, 2, 3, 4, 5],
                     lambda x: x.aggregate(lambda acc, item: acc + item, 0, lambda result: f"Sum: {result}"),
                     "Sum: 15")

def test_aggregate_seed_result_builds_dict_and_gets_count() -> None:
    lists_value_test(["apple", "banana", "apple", "cherry", "banana", "apple"],
                     lambda x: x.aggregate(lambda acc, item: {**acc, item: acc.get(item, 0) + 1}, dict[str, int](), lambda result: result.get("apple", 0)),
                     3)

def test_aggregate_seed_result_collects_and_joins() -> None:
    lists_value_test([1, 2, 3, 4, 5],
                     lambda x: x.aggregate(lambda acc, item: acc + [str(item * item)], list[str](), lambda squares: " + ".join(squares)),
                     "1 + 4 + 9 + 16 + 25")

def test_aggregate_seed_result_works_with_empty_sequence() -> None:
    lists_value_test(list[int](),
                     lambda x: x.aggregate(lambda acc, item: acc + item, 0, lambda result: f"Result: {result}"),
                     "Result: 0")

def test_aggregate_seed_result_calculates_average() -> None:
    lists_value_test([2, 4, 6, 8],
                     lambda x: x.aggregate(lambda acc, item: {"sum": acc["sum"] + item, "count": acc["count"] + 1}, {"sum": 0, "count": 0}, lambda result: result["sum"] / result["count"] if result["count"] > 0 else 0),
                     5.0)

def test_aggregate_with_different_types() -> None:
    lists_value_test([1, 2, 3, 4, 5],
                     lambda x: x.aggregate(lambda acc, item: acc + str(item), "", lambda result: int(result)),
                     12345)
