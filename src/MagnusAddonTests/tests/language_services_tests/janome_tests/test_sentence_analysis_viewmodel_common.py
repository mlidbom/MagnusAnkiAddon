from __future__ import annotations

from typing import TYPE_CHECKING

from note.sentences.sentence_configuration import SentenceConfiguration
from note.sentences.sentencenote import SentenceNote
from sysutils import ex_sequence
from sysutils.lazy import Lazy
from ui.web.sentence.sentence_viewmodel import SentenceAnalysisViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
    from ui.web.sentence.match_viewmodel import MatchViewModel

def surface_and_match_form(match_vm: MatchViewModel) -> str:
    return f"""{match_vm.match.parsed_form}:{match_vm.vocab_form}""" if match_vm.display_vocab_form else match_vm.match.parsed_form

def assert_display_words_equal_and_that_failed_matches_have_proper_messages(sentence: str, excluded: list[WordExclusion], expected_output: list[str]) -> None:

    def run_note_assertions(message: str) -> None:
        analysis = SentenceAnalysisViewModel(sentence_note)

        root_words = [surface_and_match_form(dm) for dm in analysis.displayed_matches]
        try:
            assert root_words == expected_output
        except AssertionError as e:
            print(f"""

---####--- {message} ---####---""")
            raise e

    sentence_note = SentenceNote.create(sentence)
    if len(excluded) == 0:
        run_note_assertions("running assertions with no exclusions")
    else:
        sentence_note.configuration._value = Lazy[SentenceConfiguration].from_value(SentenceConfiguration.from_hidden_matches(excluded))  # pyright: ignore[reportPrivateUsage]
        run_note_assertions("running assertions with exclusions hidden")

        sentence_note.configuration._value = Lazy[SentenceConfiguration].from_value(SentenceConfiguration.from_incorrect_matches(excluded))  # pyright: ignore[reportPrivateUsage]
        run_note_assertions("running assertions with exclusions marked as incorrect matches")

def assert_all_words_equal(sentence: str, expected_output: list[str]) -> None:
    sentence_note = SentenceNote.create(sentence)
    analysis = SentenceAnalysisViewModel(sentence_note)
    candidate_words = analysis.analysis.candidate_words
    matches = ex_sequence.flatten([cand.matches for cand in candidate_words])

    root_words = [surface_and_match_form(match) for match in matches]
    assert root_words == expected_output
