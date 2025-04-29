from typing_extensions import Any

def not_none(value:Any, message:str = "") -> None:
    if not value: raise AssertionError(message)