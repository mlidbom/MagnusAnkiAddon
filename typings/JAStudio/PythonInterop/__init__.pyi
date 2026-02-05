import typing, abc
from System.Collections.Generic import Dictionary_2
from System import Action_1

class PythonDotNetShim(abc.ABC):
    @staticmethod
    def ToDotNetDict(pythonDict: typing.Any) -> Dictionary_2[str, typing.Any]: ...
    @staticmethod
    def ToDotNetDictAction(pythonCallable: typing.Any) -> Action_1[Dictionary_2[str, typing.Any]]: ...

