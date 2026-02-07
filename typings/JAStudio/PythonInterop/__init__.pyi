import typing, abc
from System import Action_1
from System.Collections.Generic import IReadOnlyList_1, List_1, Dictionary_2, IReadOnlyDictionary_2

class PythonDotNetShim(abc.ABC):

    class Action(abc.ABC):
        # Skipped ToDotNet due to it being static, abstract and generic.

        ToDotNet : ToDotNet_MethodGroup
        class ToDotNet_MethodGroup:
            def __getitem__(self, t:typing.Type[ToDotNet_1_T1]) -> ToDotNet_1[ToDotNet_1_T1]: ...

            ToDotNet_1_T1 = typing.TypeVar('ToDotNet_1_T1')
            class ToDotNet_1(typing.Generic[ToDotNet_1_T1]):
                ToDotNet_1_T = PythonDotNetShim.Action.ToDotNet_MethodGroup.ToDotNet_1_T1
                def __call__(self, action: typing.Any) -> Action_1[ToDotNet_1_T]:...




    class LongList(abc.ABC):
        @staticmethod
        def ToPython(items: IReadOnlyList_1[int]) -> typing.Any: ...


    class StringList(abc.ABC):
        @staticmethod
        def ToDotNet(pythonList: typing.Any) -> List_1[str]: ...
        @staticmethod
        def ToPython(list: IReadOnlyList_1[str]) -> typing.Any: ...


    class StringStringDict(abc.ABC):
        @staticmethod
        def ToDotNet(pythonDict: typing.Any) -> Dictionary_2[str, str]: ...
        @staticmethod
        def ToPython(dict: IReadOnlyDictionary_2[str, str]) -> typing.Any: ...


