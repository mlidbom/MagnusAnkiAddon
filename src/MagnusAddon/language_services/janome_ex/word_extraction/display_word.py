from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord

class DisplayWord:
    def __init__(self, candidate: CandidateWord, is_surface: bool):
        self.candidate = candidate
        self.is_surface = is_surface
        if is_surface:
            self.word = candidate.surface
            self.vocabs = candidate.surface_vocabs
        else:
            self.word = candidate.base
            self.vocabs = candidate.base_vocabs

    def __repr__(self) -> str:
        return f"""{self.word}"""