import abc
from JAStudio.Core import CoreApp

class TestCoreApp:
    @staticmethod
    def Reset() -> CoreApp: ...


class TestEnvDetector(abc.ABC):
    @classmethod
    @property
    def IsTesting(cls) -> bool: ...

