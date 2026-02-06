from JAStudio.Core.Note import KanjiNote, JPNote
from System.Collections.Generic import List_1
from JAStudio.Core.UI.Web import PreRenderingContentRenderer_1

class DependenciesRenderer:
    @staticmethod
    def RenderDependenciesList(note: KanjiNote) -> str: ...


class KanjiListRenderer:
    @staticmethod
    def KanjiKanjiList(kanji: KanjiNote) -> str: ...
    @staticmethod
    def RenderList(note: JPNote, kanjis: List_1[KanjiNote], kanjiReadings: List_1[str]) -> str: ...


class KanjiNoteRenderer:
    @staticmethod
    def CreateRenderer() -> PreRenderingContentRenderer_1[KanjiNote]: ...


class MnemonicRenderer:
    @staticmethod
    def RenderMnemonic(note: KanjiNote) -> str: ...


class ReadingsRenderer:
    @staticmethod
    def RenderKatakanaOnyomi(kanjiNote: KanjiNote) -> str: ...


class VocabListRenderer:
    @staticmethod
    def GenerateVocabHtmlList(kanjiNote: KanjiNote) -> str: ...

