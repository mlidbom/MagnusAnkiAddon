import typing, abc
from System import IDisposable
from Microsoft.Data.Sqlite import SqliteConnection
from System.Collections.Generic import List_1
from JAStudio.Core.Note.Collection import CardStudyingStatus
from JAStudio.Core.Note import NetNoteData

class AnkiCardOperations:
    def SetImplementation(self, implementation: IAnkiCardOperations) -> None: ...
    def SuspendAllCardsForNote(self, noteId: int) -> None: ...
    def UnsuspendAllCardsForNote(self, noteId: int) -> None: ...


class AnkiCardOperationsImpl(IAnkiCardOperations):
    def __init__(self) -> None: ...
    def SuspendAllCardsForNote(self, noteId: int) -> None: ...
    def UnsuspendAllCardsForNote(self, noteId: int) -> None: ...


class AnkiDatabase(IDisposable):
    @property
    def Connection(self) -> SqliteConnection: ...
    def Dispose(self) -> None: ...
    @staticmethod
    def OpenReadOnly(dbFilePath: str) -> AnkiDatabase: ...


class AnkiFacade(abc.ABC):
    @staticmethod
    def GetNoteIdFromCardId(cardId: int) -> int: ...

    class Batches(abc.ABC):
        @staticmethod
        def ConvertImmersionKitSentences() -> None: ...


    class Browser(abc.ABC):
        @staticmethod
        def ExecuteLookup(query: str) -> None: ...
        @staticmethod
        def ExecuteLookupAndShowPreviewer(query: str) -> None: ...

        class MenuActions(abc.ABC):
            @staticmethod
            def PrioritizeCards(cardIds: List_1[int]) -> None: ...
            @staticmethod
            def SpreadCardsOverDays(cardIds: List_1[int], startDay: int, daysApart: int) -> None: ...



    class Col(abc.ABC):
        @staticmethod
        def DbFilePath() -> str: ...


    class NoteEx(abc.ABC):
        @staticmethod
        def SuspendAllCardsForNote(noteId: int) -> None: ...
        @staticmethod
        def UnsuspendAllCardsForNote(noteId: int) -> None: ...


    class UIUtils(abc.ABC):
        @staticmethod
        def Refresh() -> None: ...
        @staticmethod
        def ShowTooltip(message: str, periodMs: int = ...) -> None: ...



class CardStudyingStatusLoader(abc.ABC):
    @staticmethod
    def FetchAll(db: AnkiDatabase) -> List_1[CardStudyingStatus]: ...


class IAnkiCardOperations(typing.Protocol):
    @abc.abstractmethod
    def SuspendAllCardsForNote(self, noteId: int) -> None: ...
    @abc.abstractmethod
    def UnsuspendAllCardsForNote(self, noteId: int) -> None: ...


class NoteBulkLoader(abc.ABC):
    @staticmethod
    def LoadAllNotesOfType(db: AnkiDatabase, noteTypeName: str) -> List_1[NetNoteData]: ...

