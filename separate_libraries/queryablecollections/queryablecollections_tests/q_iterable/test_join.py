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

class TestJoin:
    def test_join_with_matching_keys_returns_combined_results(self) -> None:
        people = [Person(1, "Alice"), Person(2, "Bob")]
        orders = [Order(101, 1, 100.0), Order(102, 2, 200.0), Order(103, 1, 150.0)]

        result = (query(people)
                  .join(orders,
                        lambda this: this.id,
                        lambda other: other.person_id,
                        lambda this, other: f"{this.name}: ${other.amount}")
                  .to_list())

        expected = ["Alice: $100.0", "Alice: $150.0", "Bob: $200.0"]
        assert result == expected

    def test_join_with_no_matching_keys_returns_empty_sequence(self) -> None:
        people = [Person(1, "Alice"), Person(2, "Bob")]
        orders = [Order(101, 3, 100.0), Order(102, 4, 200.0)]

        result = (query(people)
                  .join(orders,
                        lambda this: this.id,
                        lambda other: other.person_id,
                        lambda this, other: f"{this.name}: ${other.amount}")
                  .to_list())

        assert result == []

    def test_join_with_empty_outer_sequence_returns_empty_sequence(self) -> None:
        people = QList[Person]()
        orders = [Order(101, 1, 100.0), Order(102, 2, 200.0)]

        result = (query(people)
                  .join(orders,
                        lambda this: this.id,
                        lambda other: other.person_id,
                        lambda this, other: f"{this.name}: ${other.amount}")
                  .to_list())

        assert result == []

    def test_join_with_empty_inner_sequence_returns_empty_sequence(self) -> None:
        people = [Person(1, "Alice"), Person(2, "Bob")]
        orders = QList[Order]()

        result = (query(people)
                  .join(orders,
                        lambda this: this.id,
                        lambda other: other.person_id,
                        lambda this, other: f"{this.name}: ${other.amount}")
                  .to_list())

        assert result == []

    def test_join_with_both_empty_sequences_returns_empty_sequence(self) -> None:
        people = QList[Person]()
        orders = QList[Order]()

        result = (query(people)
                  .join(orders,
                        lambda this: this.id,
                        lambda other: other.person_id,
                        lambda this, other: f"{this.name}: ${other.amount}")
                  .to_list())

        assert result == []

    def test_join_with_simple_types_works_correctly(self) -> None:
        numbers = [1, 2, 3, 2]
        letters = ["a", "1a", "c", "3a", "2a", "4a"]

        result = (query(numbers)
                  .join(letters,
                        lambda this: str(this),
                        lambda other: other[0],
                        lambda this, other: f"{this}-{other}")
                  .to_list())

        assert result == ["1-1a", "2-2a", "3-3a", "2-2a"]

    def test_join_with_different_key_types_works_correctly(self) -> None:
        # Test with string keys
        categories = [("tech", "Technology"), ("health", "Health")]
        products = [("laptop", "tech"), ("tablet", "tech"), ("vitamins", "health")]

        result = (query(categories)
                  .join(products,
                        lambda this: this[0],  # category id
                        lambda other: other[1],  # product category
                        lambda this, other: f"{other[0]} in {this[1]}")
                  .to_list())

        expected = ["laptop in Technology", "tablet in Technology", "vitamins in Health"]
        assert result == expected

    def test_join_is_lazy(self) -> None:
        call_count = 0

        def counting_result_selector(p: Person, o: Order) -> str:
            nonlocal call_count
            call_count += 1
            return f"{p.name}: ${o.amount}"

        people = [Person(1, "Alice"), Person(2, "Bob")]
        orders = [Order(101, 1, 100.0), Order(102, 2, 200.0)]

        joined = query(people).join(orders,
                                    lambda this: this.id,
                                    lambda other: other.person_id,
                                    counting_result_selector)

        assert call_count == 0

        result = joined.to_list()
        assert call_count == 2
        assert result == ["Alice: $100.0", "Bob: $200.0"]

    def test_join_with_none_keys_match_each_other(self) -> None:
        people = [Person(1, "Alice"), Person(None, "Bob")]
        orders = [Order(101, 1, 100.0), Order(102, None, 200.0)]  # type: ignore

        result = (query(people)
                  .join(orders,
                        lambda this: this.id,
                        lambda other: other.person_id,
                        lambda this, other: f"{this.name}: ${other.amount}")
                  .to_list())

        expected = ["Alice: $100.0", "Bob: $200.0"]
        assert result == expected

    def test_join_with_duplicate_keys_in_outer_sequence(self) -> None:
        people = [Person(1, "Alice"), Person(1, "Alice2"), Person(2, "Bob")]
        orders = [Order(101, 1, 100.0), Order(102, 2, 200.0)]

        result = (query(people)
                  .join(orders,
                        lambda this: this.id,
                        lambda other: other.person_id,
                        lambda this, other: f"{this.name}: ${other.amount}")
                  .to_list())

        expected = ["Alice: $100.0", "Alice2: $100.0", "Bob: $200.0"]
        assert result == expected
