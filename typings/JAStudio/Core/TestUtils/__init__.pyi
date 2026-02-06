
class TestApp:
    @staticmethod
    def Initialize() -> None: ...
    @staticmethod
    def Reset() -> None: ...


class TestEnvDetector:
    @classmethod
    @property
    def IsTesting(cls) -> bool: ...

