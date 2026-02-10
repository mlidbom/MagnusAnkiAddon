import typing, abc

class Easing(IEasing, abc.ABC):
    @abc.abstractmethod
    def Ease(self, progress: float) -> float: ...
    @staticmethod
    def Parse(e: str) -> Easing: ...


class IEasing(typing.Protocol):
    @abc.abstractmethod
    def Ease(self, progress: float) -> float: ...

