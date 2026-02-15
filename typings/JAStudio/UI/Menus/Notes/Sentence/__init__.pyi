import abc
from JAStudio.UI.Menus.UIAgnosticMenuStructure import SpecMenuItem
from JAStudio.Core.Note.Sentences import SentenceNote

class SentenceStringMenus(abc.ABC):
    @staticmethod
    def BuildStringMenuSpec(sentence: SentenceNote, menuString: str) -> SpecMenuItem: ...

