# queryablecollections/queryablecollections_tests/q_iterable/test.py
from __future__ import annotations

import pytest
from queryablecollections.q_errors import ArgumentError
from queryablecollections.q_iterable import QIterable


def test_repeats_element_specified_number_of_times() -> None:
    assert QIterable.repeat("x", 4).to_list() == ["x", "x", "x", "x"]

def test_with_zero_returns_empty_sequence() -> None:
    assert QIterable.repeat(42, 0).to_list() == []

def test_works_with_none() -> None:
    assert QIterable.repeat(None, 3).to_list() == [None, None, None]

def test_negative_count_raises_argument_error() -> None:
    with pytest.raises(ArgumentError):
        QIterable.repeat("x", -1).to_list()