import abc

class TestApp:
    @staticmethod
    def Initialize() -> None: ...
    @staticmethod
    def Reset() -> None: ...


class TestEnvDetector(abc.ABC):
    @classmethod
    @property
    def IsTesting(cls) -> bool: ...

