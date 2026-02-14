import typing, abc
from JAStudio.Core.Note import JPNote

class IMediaSyncService(typing.Protocol):
    @abc.abstractmethod
    def SyncMedia(self, note: JPNote) -> None: ...


class MediaSyncService(IMediaSyncService):
    def __init__(self, ankiMediaDir: str, databaseDir: str) -> None: ...
    def SyncMedia(self, note: JPNote) -> None: ...


class NullMediaSyncService(IMediaSyncService):
    def __init__(self) -> None: ...
    def SyncMedia(self, note: JPNote) -> None: ...

