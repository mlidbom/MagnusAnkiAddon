from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


def test_group_by_basic() -> None:
    data = ["apple", "apricot", "banana", "blueberry", "cherry"]

    groups = query(data).group_by(lambda x: x[0]).to_list()

    assert len(groups) == 3

    a_group = groups.single(lambda group: group.key == "a")
    b_group = groups.single(lambda group: group.key == "b")
    c_group = groups.single(lambda group: group.key == "c")

    assert sorted(a_group.elements) == ["apple", "apricot"]
    assert sorted(b_group.elements) == ["banana", "blueberry"]
    assert sorted(c_group.elements) == ["cherry"]

def test_group_by_with_element_selector() -> None:
    data = ["apple", "apricot", "banana", "blueberry", "cherry"]

    groups = (query(data)
              .group_by_with_element_selector(lambda x: x[0], lambda x: len(x))
              .to_list())

    assert len(groups) == 3

    a_group = groups.single(lambda group: group.key == "a")
    assert sorted(a_group.elements) == [5, 7]  # apple=5, apricot=7

def test_group_by_with_result_selector() -> None:
    data = ["apple", "apricot", "banana", "blueberry", "cherry"]

    result = (query(data)
              .group_by_with_result_selector(
            lambda x: x[0],
            lambda g: f"{g.key}: {len(g.elements)} items"
    )
              .to_list())

    result_set = set(result)
    expected = {"a: 2 items", "b: 2 items", "c: 1 items"}
    assert result_set == expected

def test_group_by_empty() -> None:
    result = QList[int]([]).group_by(lambda x: x).to_list()
    assert result == []

def test_group_by_with_numbers() -> None:
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    groups = query(numbers).group_by(lambda x: x % 3).to_list()

    assert len(groups) == 3

    groups.sort(key=lambda g: g.key)

    assert groups[0].key == 0
    assert sorted(groups[0].elements) == [3, 6, 9]

    assert groups[1].key == 1
    assert sorted(groups[1].elements) == [1, 4, 7, 10]

    assert groups[2].key == 2
    assert sorted(groups[2].elements) == [2, 5, 8]
