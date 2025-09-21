from __future__ import annotations

import pytest
from queryablecollections.collections.q_list import QList
from queryablecollections.q_errors import ArgumentNoneError
from queryablecollections.q_iterable import query


class DummyObj:
    def __init__(self, name: str, val: int) -> None:
        self.name: str = name
        self.val: int = val

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DummyObj) and self.name == other.name and self.val == other.val

class TestToDictFromKeyValueTypedIterable:
    """Tests for to_dict() method when called without selectors on sequences of tuples"""

    def test_with_no_arguments_returns_dict_mapping_all_keys_to_values(self) -> None:
        assert query([("a", 1),
                      ("b", 2),
                      ("c", 3)]).to_dict() == {"a": 1,
                                               "b": 2,
                                               "c": 3}

    def test_to_dict_from_empty_sequence_returns_empty_dict(self) -> None:
        assert QList[tuple[int, str]]().to_dict() == {}

    def test_to_dict_from_single_tuple_returns_single_entry_dict(self) -> None:
        assert query([("key", "value")]).to_dict() == {"key": "value"}

    def test_to_dict_with_mixed_types_preserves_types(self) -> None:
        tuple_list: list[tuple[str | int | bool, int | str | bool]] = \
            [("str_key", 42),
             (123, "str_value"),
             (True, False)]
        assert query(tuple_list).to_dict() == {"str_key": 42,
                                               123: "str_value",
                                               True: False}

    def test_to_dict_with_duplicate_keys_uses_last_value(self) -> None:
        assert query([("key", 1),
                      ("key", 2),
                      ("key", 3)]).to_dict() == {"key": 3}

class TestToDictWithSelectors:
    """Tests for to_dict() method when called with key and value selectors"""

    def test_to_dict_with_selectors_returns_a_dict_combining_the_selected_keys_and_values(self) -> None:
        assert (query([DummyObj("x", 10),
                       DummyObj("y", 14),
                       DummyObj("z", 16)])
                .to_dict(lambda o: o.name, lambda o: o.val) == {"x": 10,
                                                                "y": 14,
                                                                "z": 16})

    def test_to_dict_with_selectors_on_empty_sequence_returns_empty_dict(self) -> None:
        assert QList[int]([]).to_dict(lambda x: x, lambda x: x) == {}

    def test_to_dict_with_selectors_on_single_item_returns_single_entry_dict(self) -> None:
        assert (query([(DummyObj("test", 42))])
                .to_dict(lambda o: o.name, lambda o: o.val) == {"test": 42})

    def test_to_dict_with_selectors_and_duplicate_keys_uses_last_value(self) -> None:
        assert (query([DummyObj("same", 1),
                       DummyObj("same", 2),
                       DummyObj("same", 3)])
                .to_dict(lambda o: o.name, lambda o: o.val) == {"same": 3})

class TestToDictErrorCases:
    """Tests for error conditions in to_dict() method"""

    def test_to_dict_with_key_selector_but_without_value_selector_raises_argument_none_error(self) -> None:
        with pytest.raises(ArgumentNoneError):
            query([DummyObj("k", 9)]).to_dict(lambda o: o.name)  # type: ignore[call-overload]

    def test_to_dict_with_value_selector_but_without_key_selector_raises_argument_none_error(self) -> None:
        with pytest.raises(ArgumentNoneError):
            query([DummyObj("k", 9)]).to_dict(None, lambda o: o.val)  # type: ignore[call-overload]

    def test_to_dict_with_none_key_selector_raises_argument_none_error(self) -> None:
        with pytest.raises(ArgumentNoneError):
            query([DummyObj("k", 9)]).to_dict(None, lambda o: o.val)  # type: ignore[arg-type]
