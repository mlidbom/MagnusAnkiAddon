from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


class DummyObj:
    def __init__(self, name: str, val: int) -> None:
        self.name: str = name
        self.val: int = val

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DummyObj) and self.name == other.name and self.val == other.val

def test_to_dict_with_selectors_returns_a_dict_combining_the_selected_keys_and_values() -> None:
    assert (query([DummyObj("x", 10),
                   DummyObj("y", 14),
                   DummyObj("z", 16)])
            .to_dict(lambda o: o.name, lambda o: o.val) == {"x": 10,
                                                            "y": 14,
                                                            "z": 16})

def test_to_dict_with_selectors_on_empty_sequence_returns_empty_dict() -> None:
    assert QList[int]([]).to_dict(lambda x: x, lambda x: x) == {}

def test_to_dict_with_selectors_on_single_item_returns_single_entry_dict() -> None:
    assert (query([(DummyObj("test", 42))])
            .to_dict(lambda o: o.name, lambda o: o.val) == {"test": 42})

def test_to_dict_with_selectors_and_duplicate_keys_uses_last_value() -> None:
    assert (query([DummyObj("same", 1),
                   DummyObj("same", 2),
                   DummyObj("same", 3)])
            .to_dict(lambda o: o.name, lambda o: o.val) == {"same": 3})
