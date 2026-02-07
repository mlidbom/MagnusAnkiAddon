import abc
from JAStudio.Core.Note import KanjiNote, JPNote
from System.Collections.Generic import List_1
from JAStudio.Core.UI.Web import PreRenderingContentRenderer_1

class DependenciesRenderer(abc.ABC):
    @staticmethod
    def RenderDependenciesList(note: KanjiNote) -> str: ...


class KanjiListRenderer:
    def KanjiKanjiList(self, kanji: KanjiNote) -> str: ...
    def RenderList(self, note: JPNote, kanjis: List_1[KanjiNote], kanjiReadings: List_1[str]) -> str: ...


class KanjiNoteRenderer(abc.ABC):
    @staticmethod
    def CreateRenderer() -> PreRenderingContentRenderer_1[KanjiNote]: ...


class MnemonicRenderer(abc.ABC):
    @staticmethod
    def RenderMnemonic(note: KanjiNote) -> str: ...


class ReadingsRenderer(abc.ABC):
    @staticmethod
    def RenderKatakanaOnyomi(kanjiNote: KanjiNote) -> str: ...


class VocabListRenderer(abc.ABC):
    @staticmethod
    def GenerateVocabHtmlList(kanjiNote: KanjiNote) -> str: ...

