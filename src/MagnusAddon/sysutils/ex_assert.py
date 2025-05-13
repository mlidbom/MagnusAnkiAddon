def that(condition:bool, message:str) -> None:
    if not condition: raise AssertionError(message)