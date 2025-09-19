from __future__ import annotations

from queryablecollections.collections.q_frozen_set import QFrozenSet
from queryablecollections.collections.q_list import QList
from queryablecollections.collections.q_sequence import QImmutableSequence, QSequence
from queryablecollections.collections.q_set import QSet
from queryablecollections.q_iterable import QIterable
from sysutils import typed


def test_iterable_empty_returns_empty_sequence_the_same_instance_each_time() -> None:
    assert QIterable[str].empty() is not None
    typed.checked_cast_generics(QIterable[str], QIterable[str].empty())
    typed.checked_cast_dynamic(QIterable[str], QIterable[str].empty())

    assert QIterable[str].empty() is QIterable.empty()

def test_sequence_empty_returns_empty_sequence_the_same_instance_each_time() -> None:
    assert QSequence[str].empty() is not None
    typed.checked_cast_generics(QSequence[str], QSequence[str].empty())
    typed.checked_cast_dynamic(QSequence[str], QSequence[str].empty())

    assert QSequence[str].empty() is QSequence.empty()

def test_list_empty_returns_empty_list_new_instance_each_time() -> None:
    assert QList[str].empty() is not None
    typed.checked_cast_generics(QList[str], QList[str].empty())
    typed.checked_cast_dynamic(QList[str], QList[str].empty())
    assert QList[str].empty() is not QList.empty()

def test_set_empty_returns_empty_set_new_instance_each_time() -> None:
    assert QSet[str].empty() is not None
    typed.checked_cast_generics(QSet[str], QSet[str].empty())
    typed.checked_cast_dynamic(QSet[str], QSet[str].empty())
    assert QSet[str].empty() is not QSet.empty()

def test_frozen_set_empty_returns_empty_set_same_instance_each_time() -> None:
    assert QFrozenSet[str].empty() is not None
    typed.checked_cast_generics(QFrozenSet[str], QFrozenSet[str].empty())
    typed.checked_cast_dynamic(QFrozenSet, QFrozenSet[str].empty())
    assert QFrozenSet[str].empty() is QFrozenSet.empty()

def test_immutable_sequence_empty_returns_empty_set_same_instance_each_time() -> None:
    assert QImmutableSequence[str].empty() is not None
    typed.checked_cast_generics(QImmutableSequence[str], QImmutableSequence[str].empty())
    typed.checked_cast_dynamic(QImmutableSequence, QImmutableSequence[str].empty())
    assert QImmutableSequence[str].empty() is QImmutableSequence.empty()

