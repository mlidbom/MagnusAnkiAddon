from __future__ import annotations

from typing import TYPE_CHECKING

from ex_autoslot import AutoSlots
from ui.web.sentence.text_analysis_viewmodel import TextAnalysisViewModel

if TYPE_CHECKING:
    from note.sentences.sentencenote import SentenceNote
    from ui.web.sentence.match_viewmodel import MatchViewModel

class SentenceViewModel(AutoSlots):
    def __init__(self, sentence: SentenceNote) -> None:
        self.sentence: SentenceNote = sentence
        self.analysis: TextAnalysisViewModel = TextAnalysisViewModel(sentence.create_analysis())
        self.displayed_matches:list[MatchViewModel] = self.analysis.displayed_matches
