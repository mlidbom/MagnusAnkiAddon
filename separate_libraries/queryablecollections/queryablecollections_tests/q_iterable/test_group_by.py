from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


def test_group_by_first_character_of_string_returns_one_group_per_unique_first_character_in_the_order_encountered() -> None:
    data = ["apple", "apricot", "banana", "blueberry", "cherry"]

    groups = query(data).group_by(lambda string: string[0]).to_list()

    assert len(groups) == 3

    a_group = groups.single(lambda group: group.key == "a")
    assert a_group == groups[0]
    b_group = groups.single(lambda group: group.key == "b")
    assert b_group == groups[1]
    c_group = groups.single(lambda group: group.key == "c")
    assert c_group == groups[2]

    assert a_group == ["apple", "apricot"]
    assert b_group == ["banana", "blueberry"]
    assert c_group == ["cherry"]

def test_group_by_first_character_of_string_with_element_selector_returns_one_group_per_unique_first_character_in_the_order_encountered_and_the_values_are_the_selected_value() -> None:
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
    assert a_group.order_by(lambda x: x).to_list() == [len("apple"), len("apricot")]  # apple=5, apricot=7
    assert b_group == [len("banana"), len("blueberry")]
    assert c_group == [len("cherry")]

def test_group_by_empty_returns_no_groups() -> None:
    result = QList[int]([]).group_by(lambda element: element).to_list()
    assert result == []
