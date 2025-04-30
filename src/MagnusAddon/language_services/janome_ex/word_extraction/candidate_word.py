from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TextLocation

class CandidateWord:
    def __init__(self, locations:list[TextLocation]):
        self.location = locations
        self.surface = "".join([t.surface for t in locations]) + ""
        self.base = "".join([t.surface for t in locations[:-1]]) + locations[-1].base

    def __repr__(self) -> str:
        return f"""CandidateWord('{self.surface}, {self.base}')"""
