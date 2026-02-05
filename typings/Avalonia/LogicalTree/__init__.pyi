import typing, clr, abc
from Avalonia.Collections import IAvaloniaReadOnlyList_1
from Avalonia.Controls import ResourcesChangedEventArgs
from System import EventArgs

class IChildIndexProvider(typing.Protocol):
    @abc.abstractmethod
    def GetChildIndex(self, child: ILogical) -> int: ...
    @abc.abstractmethod
    def TryGetTotalCount(self, count: clr.Reference[int]) -> bool: ...


class ILogical(typing.Protocol):
    @property
    def IsAttachedToLogicalTree(self) -> bool: ...
    @property
    def LogicalChildren(self) -> IAvaloniaReadOnlyList_1[ILogical]: ...
    @property
    def LogicalParent(self) -> ILogical: ...
    @abc.abstractmethod
    def NotifyAttachedToLogicalTree(self, e: LogicalTreeAttachmentEventArgs) -> None: ...
    @abc.abstractmethod
    def NotifyDetachedFromLogicalTree(self, e: LogicalTreeAttachmentEventArgs) -> None: ...
    @abc.abstractmethod
    def NotifyResourcesChanged(self, e: ResourcesChangedEventArgs) -> None: ...


class ILogicalRoot(ILogical, typing.Protocol):
    pass


class LogicalTreeAttachmentEventArgs(EventArgs):
    def __init__(self, root: ILogicalRoot, source: ILogical, parent: ILogical) -> None: ...
    @property
    def Parent(self) -> ILogical: ...
    @property
    def Root(self) -> ILogicalRoot: ...
    @property
    def Source(self) -> ILogical: ...

