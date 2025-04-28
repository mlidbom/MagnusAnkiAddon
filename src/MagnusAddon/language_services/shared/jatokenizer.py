from abc import ABC, abstractmethod

from language_services.shared.jatokenizedtext import JATokenizedText

class JATokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> JATokenizedText: pass
