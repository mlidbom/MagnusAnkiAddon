import typing, abc
from System import IDisposable, IEquatable_1
from Avalonia import Rect, Point
from Avalonia.Media import ImmediateDrawingContext

class ICustomDrawOperation(IDisposable, IEquatable_1[ICustomDrawOperation], typing.Protocol):
    @property
    def Bounds(self) -> Rect: ...
    @abc.abstractmethod
    def HitTest(self, p: Point) -> bool: ...
    @abc.abstractmethod
    def Render(self, context: ImmediateDrawingContext) -> None: ...

