from __future__ import annotations

from common_helpers import throws_test, value_test
from queryablecollections.q_errors import ArgumentError


def test_divides_evenly_into_chunks_of_the_given_size_preserving_order() -> None:
    value_test([1, 2, 3, 4, 5, 6],
               lambda x: x.chunk(2).to_list(),
               [[1, 2], [3, 4], [5, 6]],
               skip_sets=True)

def test_with_remainder_includes_partial_last_chunk() -> None:
    value_test([1, 2, 3, 4, 5],
               lambda x: x.chunk(2).to_list(),
               [[1, 2], [3, 4], [5]],
               skip_sets=True)

def test_with_size_larger_than_collection_returns_single_chunk() -> None:
    value_test([1, 2, 3],
               lambda x: x.chunk(5).to_list(),
               [[1, 2, 3]],
               skip_sets=True)

def test_with_chunk_size_one_returns_individual_elements() -> None:
    value_test([1, 2, 3],
               lambda x: x.chunk(1).to_list(),
               [[1], [2], [3]],
               skip_sets=True)

def test_with_empty_collection_returns_empty() -> None:
    value_test(list[int](),
               lambda x: x.chunk(2).to_list(),
               list[int](),
               skip_sets=True)

def test_chunk_with_mixed_types() -> None:
    value_test([1, "a", 2.5, True, None],
               lambda x: x.chunk(2).to_list(),
               [[1, "a"], [2.5, True], [None]],
               skip_sets=True)

def test_chunk_size_zero_raises_argument_error() -> None:
    throws_test([1, 2, 3],
                lambda x: x.chunk(0).to_list(),
                ArgumentError,
                skip_sets=True)

def test_chunk_negative_size_raises_argument_error() -> None:
    throws_test([1, 2, 3],
                lambda x: x.chunk(-1).to_list(),
                ArgumentError,
                skip_sets=True)

def test_chunk_with_single_element_returns_single_chunk() -> None:
    value_test([42],
               lambda x: x.chunk(1).to_list(),
               [[42]],
               skip_sets=True)