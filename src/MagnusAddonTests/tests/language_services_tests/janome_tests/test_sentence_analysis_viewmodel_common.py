from __future__ import annotations

from typing import TYPE_CHECKING

from note.sentences.sentence_configuration import SentenceConfiguration
from note.sentences.sentencenote import SentenceNote
from sysutils import ex_sequence
from sysutils.lazy import Lazy
from ui.web.sentence.sentence_viewmodel import SentenceAnalysisViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

def _run_assertions(sentence: str, excluded: list[WordExclusion], expected_output: list[str]) -> None:
    def run_note_assertions(message: str | None = None) -> None:
        if message: print(message)
        analysis = SentenceAnalysisViewModel(sentence_note)
        candidate_words = analysis.analysis.candidate_words
        display_forms = ex_sequence.flatten([cand.display_forms for cand in candidate_words])
        displayed_forms = [display_form for display_form in display_forms if display_form.is_displayed]

        root_words = [df.parsed_form for df in displayed_forms]
        assert root_words == expected_output

    print()
    sentence_note = SentenceNote.create(sentence)
    if len(excluded) == 0:
        run_note_assertions()
    else:
        sentence_note.configuration._value = Lazy.from_value(SentenceConfiguration.from_incorrect_matches(excluded))
        run_note_assertions("################################### running assertions with exclusions marked as incorrect matches")

        sentence_note.configuration._value = Lazy.from_value(SentenceConfiguration.from_hidden_matches(excluded))
        run_note_assertions("################################### running assertions with exclusions hidden")
