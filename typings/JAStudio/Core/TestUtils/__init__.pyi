
class ExPytest:
    @classmethod
    @property
    def IsTesting(cls) -> bool: ...


class TestApp:
    @staticmethod
    def Initialize() -> None: ...
    @staticmethod
    def Reset() -> None: ...

