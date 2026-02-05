import typing, abc
from System.Collections.Generic import IEnumerable_1
from System import IDisposable, Func_1, Action

class Dyn(abc.ABC):
    @staticmethod
    def Enumerate(obj: typing.Any) -> IEnumerable_1[typing.Any]: ...


class PythonEnvironment(abc.ABC):
    @staticmethod
    def EnsureInitialized(venvPath: str = ...) -> None: ...
    @staticmethod
    def LockGil() -> IDisposable: ...
    # Skipped Use due to it being static, abstract and generic.

    Use : Use_MethodGroup
    class Use_MethodGroup:
        def __getitem__(self, t:typing.Type[Use_1_T1]) -> Use_1[Use_1_T1]: ...

        Use_1_T1 = typing.TypeVar('Use_1_T1')
        class Use_1(typing.Generic[Use_1_T1]):
            Use_1_TResult = PythonEnvironment.Use_MethodGroup.Use_1_T1
            def __call__(self, func: Func_1[Use_1_TResult]) -> Use_1_TResult:...

        def __call__(self, action: Action) -> None:...


