
from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import cast

import pytest
from queryablecollections.collections.q_frozen_set import QFrozenSet
from queryablecollections.collections.q_list import QList
from queryablecollections.collections.q_sequence import QImmutableSequence
from queryablecollections.collections.q_set import QSet
from queryablecollections.q_iterable import QIterable, query


def create_sequences[T](iterable: Iterable[T] | Callable[[], Iterable[T]], skip_sets: bool = False) -> list[tuple[str, QIterable[T]]]:
    factory: Callable[[], Iterable[T]] = (iterable
                                          if not isinstance(iterable, Iterable)
                                          else lambda: cast(Iterable[T], iterable))  # pyright: ignore[reportUnnecessaryCast] while basedpyright understands it is not needed, pyright does not

    values = [
            ("linq", query(factory())),
            ("QList", QList(factory())),
            ("QIterable.create", QIterable[T].create(factory())),
            ("QImmutableSequence", QImmutableSequence(list(factory()))),
    ]
    if not skip_sets:
        values += [("QSet", QSet(factory())),
                   ("QFRozenSet", QFrozenSet(factory()))]
    return values

def where_test[TIn, TOut](items: Iterable[TIn],
                          selector: Callable[[TIn], bool],
                          expected_output: list[TOut],
                          skip_sets: bool = False) -> None:
    for name, sequence in create_sequences(items, skip_sets):
        result = sequence.where(selector)
        assert result.to_list() == expected_output, name

def select_test[TIn, TOut](items: Iterable[TIn],
                           selector: Callable[[TIn], TOut],
                           expected_output: list[TOut],
                           skip_sets: bool = False) -> None:
    for name, sequence in create_sequences(items, skip_sets):
        result = sequence.select(selector)
        assert result.to_list() == expected_output, name

def value_test[TIn, TOut](items: list[TIn] | Callable[[], Iterable[TIn]],
                          selector: Callable[[QIterable[TIn]], TOut],
                          expected_output: TOut,
                          skip_sets: bool = False) -> None:
    for _name, sequence in create_sequences(items, skip_sets):
        result = selector(sequence)
        assert result == expected_output

def throws_test[TIn, TOut](items: Iterable[TIn],
                           selector: Callable[[QIterable[TIn]], TOut],
                           exception_type: type[Exception] = Exception,
                           skip_sets: bool = False) -> None:
    for name, sequence in create_sequences(items, skip_sets):
        with pytest.raises(exception_type):  # noqa: PT012
            selector(sequence)
            pytest.fail(f"{name}: Expected {exception_type} to be raised")

class CallCounter:
    def __init__(self) -> None:
        self.call_count: int = 0

    def increment(self) -> None:
        self.call_count += 1
