import abc
from JAStudio.Core import TemporaryServiceCollection
from JAStudio.UI.Menus.UIAgnosticMenuStructure import SpecMenuItem
from JAStudio.Core.Note.Sentences import SentenceNote

class SentenceNoteMenus:
    def __init__(self, services: TemporaryServiceCollection) -> None: ...
    def BuildNoteActionsMenuSpec(self, sentence: SentenceNote) -> SpecMenuItem: ...
    def BuildViewMenuSpec(self) -> SpecMenuItem: ...


class SentenceStringMenus(abc.ABC):
    @staticmethod
    def BuildStringMenuSpec(sentence: SentenceNote, menuString: str) -> SpecMenuItem: ...

