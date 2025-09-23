from __future__ import annotations

from test_common_helpers import lists_value_test


def test_excludes_elements_whose_keys_are_present_in_other_without_changing_order() -> None:
    data = [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")]
    lists_value_test(data,
                     lambda x: x.qexcept_by([3, 4, 6, 7], lambda item: item[0]).to_list(),
                     [(1, "a"), (2, "b"), (5, "e")],
                     )

def test_removes_duplicates_by_key_from_result_keeping_the_first_encountered() -> None:
    data = [("apple", 1), ("apricot", 2), ("banana", 3), ("avocado", 4)]
    # key is the first character
    lists_value_test(data,
                     lambda x: x.qexcept_by(["b"], lambda item: item[0][0]).to_list(),
                     [("apple", 1)],  # only the first 'a*' remains, 'banana' excluded, 'avocado' removed as duplicate key 'a'
                     )

def test_with_empty_other_returns_distinct_by_key_of_first() -> None:
    data = [(1, "x"), (2, "y"), (2, "z"), (3, "w")]
    lists_value_test(data,
                     lambda x: x.qexcept_by([], lambda item: item[0]).to_list(),
                     [(1, "x"), (2, "y"), (3, "w")])

def test_with_empty_first_returns_empty() -> None:
    lists_value_test(list[tuple[int, str]](),
                     lambda x: x.qexcept_by([1, 2, 3], lambda item: item[0]).to_list(),
                     list[tuple[int, str]]())

def test_with_no_matching_keys_returns_distinct_by_key_from_first() -> None:
    data = [(1, "one"), (2, "two"), (2, "two2"), (3, "three")]
    lists_value_test(data,
                     lambda x: x.qexcept_by([4, 5, 6], lambda item: item[0]).to_list(),
                     [(1, "one"), (2, "two"), (3, "three")])

def test_with_all_matching_keys_returns_empty() -> None:
    data = [(1, "a"), (2, "b"), (3, "c")]
    lists_value_test(data,
                     lambda x: x.qexcept_by([1, 2, 3, 4], lambda item: item[0]).to_list(),
                     list[tuple[int, str]]())

def test_works_with_strings_and_string_keys() -> None:
    data = ["apple", "banana", "cherry", "date", "apricot"]
    lists_value_test(data,
                     lambda x: x.qexcept_by(["b", "d"], lambda s: s[0]).to_list(),
                     ["apple", "cherry"])  # 'apricot' removed because duplicate key 'a'

def test_handles_none_keys() -> None:
    data = [("a", 1), (None, 2), ("b", 3), (None, 4)]
    lists_value_test(data,
                     lambda x: x.qexcept_by([None], lambda item: item[0]).to_list(),
                     [("a", 1), ("b", 3)])

def test_none_keys_are_distinct_by_key_when_not_excluded() -> None:
    data = [("a", 1), (None, 2), ("b", 3), (None, 4)]
    lists_value_test(data,
                     lambda x: x.qexcept_by([], lambda item: item[0]).to_list(),
                     [("a", 1), (None, 2), ("b", 3)])