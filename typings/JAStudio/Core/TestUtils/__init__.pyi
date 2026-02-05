import abc

class ExPytest(abc.ABC):
    @classmethod
    @property
    def IsTesting(cls) -> bool: ...


class TestApp(abc.ABC):
    @staticmethod
    def Initialize() -> None: ...
    @staticmethod
    def Reset() -> None: ...

