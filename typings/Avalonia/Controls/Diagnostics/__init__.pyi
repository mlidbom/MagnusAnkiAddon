import typing
from Avalonia.Controls.Primitives import IPopupHost

class IPopupHostProvider(typing.Protocol):
    @property
    def PopupHost(self) -> IPopupHost: ...

