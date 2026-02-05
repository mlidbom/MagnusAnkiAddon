import typing, abc
from System import Func_1

class LazyCE_GenericClasses(abc.ABCMeta):
    Generic_LazyCE_GenericClasses_LazyCE_1_TValue = typing.TypeVar('Generic_LazyCE_GenericClasses_LazyCE_1_TValue')
    def __getitem__(self, types : typing.Type[Generic_LazyCE_GenericClasses_LazyCE_1_TValue]) -> typing.Type[LazyCE_1[Generic_LazyCE_GenericClasses_LazyCE_1_TValue]]: ...

LazyCE : LazyCE_GenericClasses

LazyCE_1_TValue = typing.TypeVar('LazyCE_1_TValue')
class LazyCE_1(typing.Generic[LazyCE_1_TValue]):
    def __init__(self, factory: Func_1[LazyCE_1_TValue]) -> None: ...
    @property
    def Value(self) -> LazyCE_1_TValue: ...
    def Reset(self) -> None: ...
    def ValueIfInitialized(self) -> LazyCE_1_TValue: ...

