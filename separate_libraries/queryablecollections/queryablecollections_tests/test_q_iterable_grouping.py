from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


def test_group_by_basic() -> None:
    data = ["apple", "apricot", "banana", "blueberry", "cherry"]

    groups = query(data).group_by(lambda string: string[0]).to_list()

    assert len(groups) == 3

    a_group = groups.single(lambda group: group.key == "a")
    assert a_group == groups[0]
    b_group = groups.single(lambda group: group.key == "b")
    assert b_group == groups[1]
    c_group = groups.single(lambda group: group.key == "c")
    assert c_group == groups[2]

    assert a_group.elements == ["apple", "apricot"]
    assert b_group.elements == ["banana", "blueberry"]
    assert c_group.elements == ["cherry"]

def test_group_by_with_element_selector() -> None:
    data = ["apple", "apricot", "banana", "blueberry", "cherry"]

    groups = (query(data)
              .group_by(lambda element: element[0], lambda element: len(element))
              .to_list())

    assert len(groups) == 3

    a_group = groups.single(lambda group: group.key == "a")
    assert a_group == groups[0]
    b_group = groups.single(lambda group: group.key == "b")
    assert b_group == groups[1]
    c_group = groups.single(lambda group: group.key == "c")
    assert c_group == groups[2]
    assert a_group.elements.ordered().to_list() == [len("apple"), len("apricot")]  # apple=5, apricot=7
    assert b_group.elements == [len("banana"), len("blueberry")]
    assert c_group.elements == [len("cherry")]

def test_group_by_empty() -> None:
    result = QList[int]([]).group_by(lambda element: element).to_list()
    assert result == []

def test_group_by_with_numbers() -> None:
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    groups = query(numbers).group_by(lambda element: element % 3).to_list()

    assert len(groups) == 3

    assert groups[0].key == 1
    assert groups[0].elements.ordered().to_list() == [1, 4, 7, 10]

    assert groups[1].key == 2
    assert groups[1].elements.ordered().to_list() == [2, 5, 8]

    assert groups[2].key == 0
    assert groups[2].elements.ordered().to_list() == [3, 6, 9]
