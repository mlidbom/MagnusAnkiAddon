from abc import ABC, abstractmethod

class JAToken(ABC):
    @abstractmethod
    def get_base_form(self) -> str: pass

    @abstractmethod
    def get_surface_form(self) -> str: pass

    @abstractmethod
    def is_inflectable_word(self) -> bool: pass

    @abstractmethod
    def is_inflected_verb(self) -> bool: pass
