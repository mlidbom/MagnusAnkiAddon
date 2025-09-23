from __future__ import annotations

from queryablecollections.collections.q_key_value_pair import KeyValuePair
from test_common_helpers import QList, lists_value_test, query


def to_tuple[TKey, TValue](x: KeyValuePair[TKey, TValue]) -> tuple[TKey, TValue]:
    return x.key, x.value


def test_count_by_returns_count_of_each_key() -> None:
    lists_value_test([1, 2, 2, 3, 3, 3],
                     lambda x: x.qcount_by(lambda y: y).select(to_tuple).to_list(),
                     [(1, 1), (2, 2), (3, 3)])

def test_count_by_with_string_keys() -> None:
    lists_value_test(["apple", "banana", "apple", "cherry", "banana", "apple"],
                     lambda x: x.qcount_by(lambda y: y).select(to_tuple).to_list(),
                     [("apple", 3), ("banana", 2), ("cherry", 1)])

def test_count_by_with_key_selector_function() -> None:
    lists_value_test(["apple", "apricot", "banana", "blueberry", "cherry"],
                     lambda x: x.qcount_by(lambda word: word[0]).select(to_tuple).to_list(),
                     [("a", 2), ("b", 2), ("c", 1)])

def test_count_by_with_length_selector() -> None:
    lists_value_test(["cat", "dog", "elephant", "ant", "bee"],
                     lambda x: x.qcount_by(lambda word: len(word)).select(to_tuple).to_list(),
                     [(3, 4), (8, 1)])

def test_count_by_empty_collection_returns_empty_result() -> None:
    lists_value_test(QList[int](),
                     lambda x: x.qcount_by(lambda y: y).select(to_tuple).to_list(),
                     QList[int]())

def test_count_by_single_element_returns_single_count() -> None:
    lists_value_test([42],
                     lambda x: x.qcount_by(lambda y: y).select(to_tuple).to_list(),
                     [(42, 1)])

def test_count_by_all_same_elements_returns_single_entry() -> None:
    lists_value_test([5, 5, 5, 5],
                     lambda x: x.qcount_by(lambda y: y).select(to_tuple).to_list(),
                     [(5, 4)])

def test_count_by_with_none_values() -> None:
    lists_value_test([1, None, 2, None, None],
                     lambda x: x.qcount_by(lambda y: y).select(to_tuple).to_list(),
                     [(1, 1), (None, 3), (2, 1)])

def test_count_by_with_boolean_selector() -> None:
    lists_value_test([1, 2, 3, 4, 5, 6],
                     lambda x: x.qcount_by(lambda y: y % 2 == 0).select(to_tuple).to_list(),
                     [(False, 3), (True, 3)])

def test_count_by_preserves_key_order_of_first_occurrence() -> None:
    lists_value_test([3, 1, 2, 1, 3, 2],
                     lambda x: x.qcount_by(lambda y: y).select(to_tuple).to_list(),
                     [(3, 2), (1, 2), (2, 2)])

def test_count_by_with_mixed_types() -> None:
    lists_value_test([1, "hello", 2.5, "hello", 1, True],
                     lambda x: x.qcount_by(lambda y: type(y).__name__).select(to_tuple).to_list(),
                     [("int", 2), ("str", 2), ("float", 1), ("bool", 1)])

def test_count_by_maintains_insertion_order() -> None:
    lists_value_test(["z", "a", "z", "b", "a", "z"],
                     lambda x: x.qcount_by(lambda y: y).select(to_tuple).to_list(),
                     [("z", 3), ("a", 2), ("b", 1)])

def test_count_by_can_be_chained_with_other_operations() -> None:
    lists_value_test([1, 2, 2, 3, 3, 3],
                     lambda x: x.qcount_by(lambda y: y).where(lambda kv: kv.value > 1).select(to_tuple).to_list(),
                     [(2, 2), (3, 3)])

def test_count_by_with_duplicate_consecutive_values() -> None:
    lists_value_test([1, 1, 2, 2, 2, 1],
                     lambda x: x.qcount_by(lambda y: y).select(to_tuple).to_list(),
                     [(1, 3), (2, 3)])

def test_count_by_with_complex_objects() -> None:
    class Person:
        def __init__(self, name: str, age: int) -> None:
            self.name = name
            self.age = age

    people = [Person("Alice", 25), Person("Bob", 30), Person("Charlie", 25), Person("Diana", 30)]
    lists_value_test(people,
                     lambda x: x.qcount_by(lambda p: p.age).select(to_tuple).to_list(),
                     [(25, 2), (30, 2)])

def test_count_by_returns_proper_key_value_pairs() -> None:
    result = query([1, 2, 2, 3]).qcount_by(lambda x: x).first()
    assert isinstance(result, KeyValuePair)
    assert result.key == 1
    assert result.value == 1
