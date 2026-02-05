from __future__ import annotations

from typing import TYPE_CHECKING

from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib.ui.web.sentence.sentence_viewmodel import SentenceViewModel

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
    from jaslib.ui.web.sentence.match_viewmodel import MatchViewModel

def surface_and_match_form(match_vm: MatchViewModel) -> str:
    form_to_display = match_vm.parsed_form
    if match_vm.vocab_match and match_vm.vocab_match.vocab.question.is_disambiguated:
        form_to_display = match_vm.vocab_match.vocab.question.disambiguation_name

    emergency = ":emergency" if match_vm.match.is_emergency_displayed else ""
    return f"""{form_to_display}:{match_vm.vocab_form}{emergency}""" if match_vm.display_vocab_form else f"{form_to_display}{emergency}"

def assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence: str, incorrect: list[WordExclusion], hidden: list[WordExclusion], expected_output: list[str]) -> None:
    def run_note_assertions(message: str) -> None:
        root_words = [surface_and_match_form(dm) for dm in sentence_view_model.displayed_matches]
        try:
            assert root_words == expected_output
        except AssertionError:
            print(f"""

---####--- {message} ---####---""")
            raise

    sentence_note = SentenceNote.create(sentence)
    for exclusion in hidden:
        sentence_note.configuration.hidden_matches.add(exclusion)
    for exclusion in incorrect:
        sentence_note.configuration.incorrect_matches.add(exclusion)


    sentence_view_model = SentenceViewModel(sentence_note)


    if len(incorrect) == 0:
        run_note_assertions("running assertions with no exclusions")
    else:
        run_note_assertions("running assertions with exclusions")

def assert_all_words_equal(sentence: str, expected_output: list[str]) -> None:
    sentence_note = SentenceNote.create(sentence)
    analysis = SentenceViewModel(sentence_note)
    candidate_words = analysis.analysis.candidate_words
    matches = (candidate_words.select_many(lambda cand: cand.matches)
               .select(surface_and_match_form)
               .to_list())

    assert matches == expected_output
