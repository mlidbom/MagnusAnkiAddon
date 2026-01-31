import typing, abc
from JAStudio.Core.Tokenization import ITokenizer
from System.Collections.Generic import List_1
from JAStudio.Core.Domain import Token

class JanomeTokenizer(ITokenizer):
    def __init__(self) -> None: ...
    @property
    def IsInitialized(self) -> bool: ...
    def InitializeFromPython(self, janomeTokenizer: typing.Any) -> None: ...
    def Tokenize(self, text: str) -> List_1[Token]: ...


class PythonEnvironment(abc.ABC):
    @classmethod
    @property
    def IsInitialized(cls) -> bool: ...
    @staticmethod
    def EnsureInitialized(venvPath: str = ...) -> None: ...

