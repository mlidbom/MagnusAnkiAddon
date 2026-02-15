import abc
from JAStudio.Core import TemporaryServiceCollection
from JAStudio.UI.Menus.UIAgnosticMenuStructure import SpecMenuItem
from JAStudio.Core.Note import KanjiNote

class KanjiNoteMenus:
    def __init__(self, services: TemporaryServiceCollection) -> None: ...
    def BuildNoteActionsMenuSpec(self, kanji: KanjiNote) -> SpecMenuItem: ...
    def BuildViewMenuSpec(self) -> SpecMenuItem: ...


class KanjiStringMenus(abc.ABC):
    @staticmethod
    def BuildStringMenuSpec(text: str, kanji: KanjiNote) -> SpecMenuItem: ...

