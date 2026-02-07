import typing, abc
from System.Collections.Generic import IReadOnlyList_1, List_1, Dictionary_2, IReadOnlyDictionary_2

class PythonDotNetShim(abc.ABC):

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


