from abc import ABC, abstractmethod
from typing import Sequence

from language_services.shared.jatoken import JAToken

class JATokenizedText(ABC):
    @abstractmethod
    def get_tokens(self) -> Sequence[JAToken]: pass
