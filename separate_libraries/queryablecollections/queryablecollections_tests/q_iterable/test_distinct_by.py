from __future__ import annotations

from test_common_helpers import value_test_including_unordered_collections


def test_distinct_by_removes_duplicates_by_selected_key_while_retaining_order_keeping_the_first_matched_value() -> None:
    value_test_including_unordered_collections([("a", 1),
                                                ("a", 2),
                                                ("b", 3),
                                                ("a", 4),
                                                ("b", 5)],
                                               lambda x: x.distinct_by(lambda y: y[0]).to_list(),
                                               [("a", 1),
                ("b", 3)],
                                               skip_sets=True)
