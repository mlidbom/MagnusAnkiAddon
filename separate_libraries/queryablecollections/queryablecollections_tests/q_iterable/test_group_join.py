from __future__ import annotations

from dataclasses import dataclass

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


@dataclass
class Person:
    id: int | None
    name: str

@dataclass
class Order:
    id: int
    person_id: int | None
    amount: float

def test_returns_groups_with_all_matching_items_in_the_order_found_for_both_inner_and_outer_items() -> None:
    people = [Person(1, "Alice"), Person(2, "Bob"), Person(3, "Charlie")]
    orders = [
            Order(101, 1, 100.0), Order(102, 1, 150.0),  # Alice's orders
            Order(103, 2, 200.0),  # Bob's order
            Order(104, 3, 75.0), Order(105, 3, 300.0)  # Charlie's orders
    ]

    result = (query(people)
              .group_join(orders,
                          lambda person: person.id,
                          lambda order: order.person_id,
                          lambda person, person_orders: f"""{person.name}: {", ".join(str(order) for order in person_orders)}""")
              .to_list())

    expected = ["Alice: Order(id=101, person_id=1, amount=100.0), Order(id=102, person_id=1, amount=150.0)",
                "Bob: Order(id=103, person_id=2, amount=200.0)",
                "Charlie: Order(id=104, person_id=3, amount=75.0), Order(id=105, person_id=3, amount=300.0)"]
    assert result == expected

def test_with_no_matching_keys_returns_empty_groups() -> None:
    people = [Person(1, "Alice"), Person(2, "Bob")]
    orders = [Order(101, 3, 100.0), Order(102, 4, 200.0)]  # No matching person IDs

    result = (query(people)
              .group_join(orders,
                          lambda person: person.id,
                          lambda order: order.person_id,
                          lambda person, person_orders: f"{person.name}: {person_orders.qcount()} orders")
              .to_list())

    expected = ["Alice: 0 orders", "Bob: 0 orders"]
    assert result == expected

def test_with_empty_outer_sequence_returns_empty_result() -> None:
    people = QList[Person]()
    orders = [Order(101, 1, 100.0), Order(102, 2, 200.0)]

    result = (query(people)
              .group_join(orders,
                          lambda person: person.id,
                          lambda order: order.person_id,
                          lambda person, person_orders: f"{person.name}: {person_orders.qcount()} orders")
              .to_list())

    assert result == []

def test_with_empty_inner_sequence_returns_all_outer_with_empty_groups() -> None:
    people = [Person(1, "Alice"), Person(2, "Bob")]
    orders = QList[Order]()

    result = (query(people)
              .group_join(orders,
                          lambda person: person.id,
                          lambda order: order.person_id,
                          lambda person, person_orders: f"{person.name}: {person_orders.qcount()} orders")
              .to_list())

    expected = ["Alice: 0 orders", "Bob: 0 orders"]
    assert result == expected

def test_with_both_empty_sequences_returns_empty_result() -> None:
    people = QList[Person]()
    orders = QList[Order]()

    result = (query(people)
              .group_join(orders,
                          lambda person: person.id,
                          lambda order: order.person_id,
                          lambda person, person_orders: f"{person.name}: {person_orders.qcount()} orders")
              .to_list())

    assert result == []

def test_items_with_none_keys_match_each_other() -> None:
    people = [Person(1, "Alice"), Person(None, "Unknown")]
    orders = [Order(101, 1, 100.0), Order(102, None, 200.0)]

    result = (query(people)
              .group_join(orders,
                          lambda person: person.id,
                          lambda order: order.person_id,
                          lambda person, person_orders: f"{person.name}: {person_orders.qcount()} orders")
              .to_list())

    expected = ["Alice: 1 orders", "Unknown: 1 orders"]
    assert result == expected

def test_duplicate_keys_in_outer_sequence_stay_duplicated_and_the_same_group_appears_in_each() -> None:
    people = [Person(1, "Alice1"), Person(1, "Alice2"), Person(2, "Bob")]
    orders = [Order(101, 1, 100.0), Order(102, 2, 200.0), Order(103, 1, 100.0)]

    result = (query(people)
              .group_join(orders,
                          lambda person: person.id,
                          lambda order: order.person_id,
                          lambda person, person_orders: f"{person.name}: {person_orders.qcount()} orders")
              .to_list())

    expected = ["Alice1: 2 orders", "Alice2: 2 orders", "Bob: 1 orders"]
    assert result == expected
