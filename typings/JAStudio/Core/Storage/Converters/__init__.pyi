import abc
from JAStudio.Core.Note import NoteData, KanjiNote, SentenceNote, VocabNote
from JAStudio.Core.Storage.Dto import KanjiNoteDto, SentenceNoteDto, VocabNoteDto

class KanjiNoteConverter(abc.ABC):
    @staticmethod
    def FromDto(dto: KanjiNoteDto) -> NoteData: ...
    @staticmethod
    def ToDto(note: KanjiNote) -> KanjiNoteDto: ...


class SentenceNoteConverter(abc.ABC):
    @staticmethod
    def FromDto(dto: SentenceNoteDto) -> NoteData: ...
    @staticmethod
    def ToDto(note: SentenceNote) -> SentenceNoteDto: ...


class VocabNoteConverter(abc.ABC):
    @staticmethod
    def FromDto(dto: VocabNoteDto) -> NoteData: ...
    @staticmethod
    def ToDto(note: VocabNote) -> VocabNoteDto: ...

