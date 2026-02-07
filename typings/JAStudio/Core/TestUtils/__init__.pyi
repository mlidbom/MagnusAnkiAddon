import abc
from JAStudio.Core import App

class TestApp:
    @staticmethod
    def Reset() -> App: ...


class TestEnvDetector(abc.ABC):
    @classmethod
    @property
    def IsTesting(cls) -> bool: ...

