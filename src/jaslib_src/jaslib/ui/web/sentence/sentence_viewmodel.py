from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.ui.web.sentence.text_analysis_viewmodel import TextAnalysisViewModel

if TYPE_CHECKING:
    from jaslib.note.sentences.sentencenote import SentenceNote
    from jaslib.ui.web.sentence.match_viewmodel import MatchViewModel

class SentenceViewModel(Slots):
    def __init__(self, sentence: SentenceNote) -> None:
        self.sentence: SentenceNote = sentence
        self.analysis: TextAnalysisViewModel = TextAnalysisViewModel(sentence.create_analysis(for_ui=True))
        self.displayed_matches:list[MatchViewModel] = self.analysis.displayed_matches
