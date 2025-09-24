from __future__ import annotations

from queryablecollections.q_iterable import query


def test_of_type_filters_by_type() -> None:
    mixed_type_values = query([1, "hello", 2.5, "world", 42, 3.14, True, False])

    assert mixed_type_values.of_type(str).to_list() == ["hello", "world"]
    assert mixed_type_values.of_type(int).to_list() == [1, 42, True, False]  # note: bool is a subclass of int in Python
    assert mixed_type_values.of_type(float).to_list() == [2.5, 3.14]

def test_of_type_with_inheritance() -> None:
    class Animal:
        def __init__(self, name: str) -> None:
            self.name: str = name

    class Dog(Animal): pass

    class Cat(Animal): pass

    mixed_animals = query([Dog("Buddy"),
                           Cat("Whiskers"),
                           Dog("Rex"),
                           Animal("Generic"),
                           Cat("Mittens")])

    dogs = mixed_animals.of_type(Dog).to_list()
    assert len(dogs) == 2
    assert all(isinstance(dog, Dog) for dog in dogs)
    assert dogs.select(lambda dog: dog.name).to_list() == ["Buddy", "Rex"]

    cats = mixed_animals.of_type(Cat).to_list()
    assert len(cats) == 2
    assert all(isinstance(cat, Cat) for cat in cats)
    assert cats.select(lambda cat: cat.name).to_list() == ["Whiskers", "Mittens"]

    all_animals = mixed_animals.of_type(Animal).to_list()
    assert len(all_animals) == 5
    assert all(isinstance(animal, Animal) for animal in all_animals)

def test_if_there_are_no_floats_of_type_float_returns_no_elements() -> None:
    assert (query([1, 2, 3, "hello", "world"]).of_type(float)
            .to_list()) == []

def test_of_type_string_returns_all_strings() -> None:
    assert (query(["apple", "banana", "cherry"])
            .of_type(str).to_list() == ["apple", "banana", "cherry"])

def test_of_type_with_none_values_only_returns_none_values_if_the_given_type_was_none() -> None:
    list_including_none_values = [1, None, "hello", None, 2.5, None]

    assert query(list_including_none_values).of_type(str).to_list() == ["hello"]

    assert query(list_including_none_values).of_type(int).to_list() == [1]

    assert query(list_including_none_values).of_type(type(None)).to_list() == [None, None, None]
