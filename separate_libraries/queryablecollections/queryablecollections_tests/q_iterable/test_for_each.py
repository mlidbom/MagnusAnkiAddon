from __future__ import annotations

from common_helpers import CallCounter, value_test


def test_executes_action_for_each_element() -> None:
    value_test(lambda: [CallCounter(), CallCounter(), CallCounter()],
               lambda x: x.for_each(lambda y: y.increment()).select(lambda y: y.call_count).to_list(),
               [1, 1, 1])
