import typing, abc
from JAStudio.Core import IBackendDataLoader, BackendData, IEnvironmentPaths
from JAStudio.Core.TaskRunners import TaskRunner
from JAStudio.Core.Note import IBackendNoteCreator, KanjiNote, SentenceNote, VocabNote, NoteData, NoteId, IAnkiCardOperations, AnkiNoteIdMap, NoteServices
from System import Action, IDisposable, Func_2, Guid
from System.Collections.Generic import List_1, Dictionary_2, IReadOnlyList_1
from Microsoft.Data.Sqlite import SqliteConnection
from JAStudio.Core.Storage import INoteRepository, AllNotesData
from JAStudio.Core.Note.Collection import CardStudyingStatus

class AnkiBackendDataLoader(IBackendDataLoader):
    def __init__(self) -> None: ...
    def Load(self, taskRunner: TaskRunner) -> BackendData: ...


class AnkiBackendNoteCreator(IBackendNoteCreator):
    def __init__(self) -> None: ...
    def CreateKanji(self, note: KanjiNote, callback: Action) -> None: ...
    def CreateSentence(self, note: SentenceNote, callback: Action) -> None: ...
    def CreateVocab(self, note: VocabNote, callback: Action) -> None: ...


class AnkiBulkLoadResult:
    def __init__(self, notes: List_1[NoteData], ankiIdMap: Dictionary_2[int, NoteId]) -> None: ...
    @property
    def AnkiIdMap(self) -> Dictionary_2[int, NoteId]: ...
    @property
    def Notes(self) -> List_1[NoteData]: ...


class AnkiCardOperationsImpl(IAnkiCardOperations):
    def __init__(self, idMap: AnkiNoteIdMap) -> None: ...
    def SuspendAllCardsForNote(self, noteId: NoteId) -> None: ...
    def UnsuspendAllCardsForNote(self, noteId: NoteId) -> None: ...


class AnkiDatabase(IDisposable):
    @property
    def Connection(self) -> SqliteConnection: ...
    def Dispose(self) -> None: ...
    @staticmethod
    def OpenReadOnly(dbFilePath: str) -> AnkiDatabase: ...


class AnkiEnvironmentPaths(IEnvironmentPaths):
    def __init__(self) -> None: ...
    @property
    def AddonRootDir(self) -> str: ...


class AnkiFacade(abc.ABC):
    @staticmethod
    def GetAddonRootDir() -> str: ...
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
            def PrioritizeCards(cardIds: IReadOnlyList_1[int]) -> None: ...
            @staticmethod
            def SpreadCardsOverDays(cardIds: IReadOnlyList_1[int], startDay: int, daysApart: int) -> None: ...



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



class AnkiLifecycleEvent(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ProfileOpened : AnkiLifecycleEvent # 0
    ProfileClosing : AnkiLifecycleEvent # 1
    SyncStarting : AnkiLifecycleEvent # 2
    SyncCompleted : AnkiLifecycleEvent # 3
    CollectionLoaded : AnkiLifecycleEvent # 4


class AnkiNoteRepository(INoteRepository):
    def __init__(self, noteServices: NoteServices) -> None: ...
    def LoadAll(self) -> AllNotesData: ...
    # Skipped Save due to it being static, abstract and generic.

    Save : Save_MethodGroup
    class Save_MethodGroup:
        @typing.overload
        def __call__(self, note: KanjiNote) -> None:...
        @typing.overload
        def __call__(self, note: VocabNote) -> None:...
        @typing.overload
        def __call__(self, note: SentenceNote) -> None:...



class CardStudyingStatusLoader(abc.ABC):
    @staticmethod
    def FetchAll(dbFilePath: str) -> List_1[CardStudyingStatus]: ...


class NoteBulkLoader(abc.ABC):
    @staticmethod
    def LoadAllNotesOfType(dbFilePath: str, noteTypeName: str, idFactory: Func_2[Guid, NoteId]) -> AnkiBulkLoadResult: ...
    @staticmethod
    def LoadAnkiIdMaps(dbFilePath: str) -> Dictionary_2[int, NoteId]: ...

