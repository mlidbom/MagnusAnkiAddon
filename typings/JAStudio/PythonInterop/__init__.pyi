import abc
from JAStudio.Core.Tokenization import ITokenizer
from System.Collections.Generic import List_1
from JAStudio.Core.Domain import Token

class JanomeTokenizer(ITokenizer):
    def __init__(self) -> None: ...
    def Tokenize(self, text: str) -> List_1[Token]: ...


class PythonEnvironment(abc.ABC):
    @staticmethod
    def EnsureInitialized(venvPath: str = ...) -> None: ...

