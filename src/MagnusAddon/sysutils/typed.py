from __future__ import annotations

def str_(value: any) -> str: return _assert_type(value, str)
def int_(value: any) -> int: return _assert_type(value, int)

def _assert_type(value: any, value_type: type) -> any:
    if not isinstance(value, value_type): raise TypeError(f"Expected type {value_type}, but got {type(value)}")
    return value