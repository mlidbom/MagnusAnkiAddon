import abc
from JAStudio.Core.Note.CorpusData import KanjiData, SentenceData, VocabData
from JAStudio.Core.Note import KanjiNote, SentenceNote, VocabNote

class KanjiNoteConverter(abc.ABC):
    @staticmethod
    def ToCorpusData(note: KanjiNote) -> KanjiData: ...


class SentenceNoteConverter(abc.ABC):
    @staticmethod
    def ToCorpusData(note: SentenceNote) -> SentenceData: ...


class VocabNoteConverter(abc.ABC):
    @staticmethod
    def ToCorpusData(note: VocabNote) -> VocabData: ...

