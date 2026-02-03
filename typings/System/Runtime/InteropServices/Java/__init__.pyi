import typing, clr, abc
from System import UIntPtr, ReadOnlySpan_1
from System.Runtime.InteropServices import GCHandle
from  import 

class ComponentCrossReference:
    DestinationGroupIndex : UIntPtr
    SourceGroupIndex : UIntPtr


class JavaMarshal(abc.ABC):
    @staticmethod
    def CreateReferenceTrackingHandle(obj: typing.Any, context: clr.Reference[None]) -> GCHandle: ...
    @staticmethod
    def FinishCrossReferenceProcessing(crossReferences: clr.Reference[MarkCrossReferencesArgs], unreachableObjectHandles: ReadOnlySpan_1[GCHandle]) -> None: ...
    @staticmethod
    def GetContext(obj: GCHandle) -> clr.Reference[None]: ...
    @staticmethod
    def Initialize(markCrossReferences: ) -> None: ...


class MarkCrossReferencesArgs:
    ComponentCount : UIntPtr
    Components : clr.Reference[StronglyConnectedComponent]
    CrossReferenceCount : UIntPtr
    CrossReferences : clr.Reference[ComponentCrossReference]


class StronglyConnectedComponent:
    Contexts : clr.Reference[clr.Reference[None]]
    Count : UIntPtr

