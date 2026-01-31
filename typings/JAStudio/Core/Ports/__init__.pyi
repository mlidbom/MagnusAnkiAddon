import typing, abc
from System.Collections.Generic import List_1
from JAStudio.Core.Domain import Token

class IJapaneseNlpProvider(typing.Protocol):
    @abc.abstractmethod
    def Tokenize(self, text: str) -> List_1[Token]: ...

