from __future__ import annotations

import pytest
from queryablecollections.q_iterable import QIterable


def test_single_argument_creates_range_from_0_to_end_minus_one() -> None:
    assert QIterable.range(5).to_list() == [0, 1, 2, 3, 4]

def test_start_and_stop_returns_start_to_end_minus_1() -> None:
    assert QIterable.range(1, 5).to_list() == [1, 2, 3, 4]

def test_with_positive_step_each_element_is_step_larger_than_the_previous() -> None:
    assert QIterable.range(0, 10, 2).to_list() == [0, 2, 4, 6, 8]

def test_with_negative_step_each_element_is_step_smaller_than_the_previous() -> None:
    assert QIterable.range(5, 0, -1).to_list() == [5, 4, 3, 2, 1]

def test_empty_when_start_equals_stop() -> None:
    assert QIterable.range(3, 3).to_list() == []

def test_step_zero_raises_value_error() -> None:
    with pytest.raises(ValueError):
        QIterable.range(0, 10, 0).to_list()

def test_returns_qintiterable_supporting_numeric_ops() -> None:
    assert QIterable.range(1, 6).sum() == 15

