import typing, abc

class AnkiCardOperations:
    @staticmethod
    def SetImplementation(implementation: IAnkiCardOperations) -> None: ...
    @staticmethod
    def SuspendAllCardsForNote(noteId: int) -> None: ...
    @staticmethod
    def UnsuspendAllCardsForNote(noteId: int) -> None: ...


class IAnkiCardOperations(typing.Protocol):
    @abc.abstractmethod
    def SuspendAllCardsForNote(self, noteId: int) -> None: ...
    @abc.abstractmethod
    def UnsuspendAllCardsForNote(self, noteId: int) -> None: ...

