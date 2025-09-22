from __future__ import annotations

from common_helpers import value_test


def test_to_list() -> None: value_test([1, 2, 3], lambda x: x.to_list(), [1, 2, 3])
def test_to_sequence() -> None: value_test([1, 2, 3], lambda x: x.to_sequence().to_list(), [1, 2, 3])
def test_to_builtin_list() -> None: value_test([1, 2, 3], lambda x: x.to_built_in_list(), [1, 2, 3])
def test_to_set() -> None: value_test([1, 2, 3], lambda x: x.to_set(), {1, 2, 3})
def test_to_frozenset() -> None: value_test([1, 2, 3], lambda x: x.to_frozenset(), frozenset({1, 2, 3}))
