from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from ui.web.sentence.text_analysis_viewmodel import TextAnalysisViewModel

if TYPE_CHECKING:
    from note.sentences.sentencenote import SentenceNote
    from ui.web.sentence.match_viewmodel import MatchViewModel

class SentenceAnalysisViewModel(Slots):
    def __init__(self, sentence: SentenceNote) -> None:
        self.sentence: SentenceNote = sentence
        self.analysis: TextAnalysisViewModel = TextAnalysisViewModel(TextAnalysis(sentence.get_question(), sentence.configuration.configuration))
        self.displayed_matches:list[MatchViewModel] = self.analysis.displayed_matches
