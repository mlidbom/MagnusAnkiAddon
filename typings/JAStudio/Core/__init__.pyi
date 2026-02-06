import abc
from System import Action
from JAStudio.Core.Note.Collection import JPCollection
from JAStudio.Core.Configuration import JapaneseConfig
from JAStudio.Core.Note import IBackendNoteCreator
from System.Collections.Generic import List_1

class App(abc.ABC):
    @classmethod
    @property
    def IsTesting(cls) -> bool: ...
    @classmethod
    @property
    def UserFilesDir(cls) -> str: ...
    @staticmethod
    def AddInitHook(hook: Action) -> None: ...
    @staticmethod
    def Col() -> JPCollection: ...
    @staticmethod
    def Config() -> JapaneseConfig: ...
    @staticmethod
    def Reset(backendNoteCreator: IBackendNoteCreator) -> None: ...


class StringExtensions(abc.ABC):
    InvisibleSpace : str
    @staticmethod
    def ExtractCommaSeparatedValues(input: str) -> List_1[str]: ...
    @staticmethod
    def FirstNumber(input: str) -> str: ...
    @staticmethod
    def PadToLength(value: str, targetLength: int, spaceScaling: float = ...) -> str: ...
    @staticmethod
    def ReplaceWord(word: str, replacement: str, text: str) -> str: ...
    @staticmethod
    def StripHtmlMarkup(input: str) -> str: ...

