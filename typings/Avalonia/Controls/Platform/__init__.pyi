import typing, abc
from Avalonia import Rect, Thickness
from Avalonia.Media import Color
from Avalonia.Controls import MenuBase

class IInputPane(typing.Protocol):
    @property
    def OccludedRect(self) -> Rect: ...
    @property
    def State(self) -> InputPaneState: ...


class IInsetsManager(typing.Protocol):
    @property
    def DisplayEdgeToEdge(self) -> bool: ...
    @DisplayEdgeToEdge.setter
    def DisplayEdgeToEdge(self, value: bool) -> bool: ...
    @property
    def IsSystemBarVisible(self) -> typing.Optional[bool]: ...
    @IsSystemBarVisible.setter
    def IsSystemBarVisible(self, value: typing.Optional[bool]) -> typing.Optional[bool]: ...
    @property
    def SafeAreaPadding(self) -> Thickness: ...
    @property
    def SystemBarColor(self) -> typing.Optional[Color]: ...
    @SystemBarColor.setter
    def SystemBarColor(self, value: typing.Optional[Color]) -> typing.Optional[Color]: ...


class IMenuInteractionHandler(typing.Protocol):
    @abc.abstractmethod
    def Attach(self, menu: MenuBase) -> None: ...
    @abc.abstractmethod
    def Detach(self, menu: MenuBase) -> None: ...


class InputPaneState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Closed : InputPaneState # 0
    Open : InputPaneState # 1

