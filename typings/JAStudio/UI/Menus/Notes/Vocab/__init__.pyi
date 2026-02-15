from JAStudio.Core import TemporaryServiceCollection
from JAStudio.UI.Menus.UIAgnosticMenuStructure import SpecMenuItem
from JAStudio.Core.Note.Vocabulary import VocabNote

class VocabStringMenus:
    def __init__(self, services: TemporaryServiceCollection) -> None: ...
    def BuildStringMenuSpec(self, text: str, vocab: VocabNote) -> SpecMenuItem: ...

