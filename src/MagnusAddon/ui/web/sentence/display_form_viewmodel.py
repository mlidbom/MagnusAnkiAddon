from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.word_extraction.vocab_match import VocabMatch
from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from ui.web.sentence.compound_part_viewmodel import CompoundPartViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.match import Match
    from note.sentences.sentence_configuration import SentenceConfiguration
    from sysutils.weak_ref import WeakRef
    from ui.web.sentence.candidate_word_viewmodel import CandidateWordViewModel


class DisplayFormViewModel:
    def __init__(self, word_viewmodel: WeakRef[CandidateWordViewModel], display_form: Match) -> None:
        self.display_form: Match = display_form
        self._config: SentenceConfiguration = word_viewmodel().candidate_word.token_range().analysis().configuration
        self.word_viewmodel: WeakRef[CandidateWordViewModel] = word_viewmodel
        self.is_shadowed: bool = word_viewmodel().is_shadowed
        self.is_display_word = word_viewmodel().is_display_word
        self.parsed_form = display_form.parsed_form
        self.answer = display_form.answer
        self.vocab_form = display_form.vocab_form
        self.compound_parts: list[CompoundPartViewModel] = []
        self.audio_path = ""
        self.is_highlighted = self.parsed_form in self._config.highlighted_words or self.vocab_form in self._config.highlighted_words
        self.readings: str = ", ".join(display_form.readings)
        self.meta_tags_html: str = ""
        self.meta_tags: str = ""
        self.display_vocab_form = False
        self.is_perfect_match = self.parsed_form == self.vocab_form
        self.display_readings = self.parsed_form != self.readings
        if isinstance(display_form, VocabMatch):
            self.compound_parts = CompoundPartViewModel.get_compound_parts_recursive(display_form.vocab, self._config)
            self.audio_path = display_form.vocab.audio.get_primary_audio_path()
            self.meta_tags = " ".join(display_form.vocab.get_meta_tags())
            self.meta_tags_html = display_form.vocab.meta_data.meta_tags_html(display_extended_sentence_statistics=False)
            if self.parsed_form != self.vocab_form:
                self.display_vocab_form = True
                self.display_readings = self.vocab_form != self.readings

        self.meta_tags += " highlighted" if self.is_highlighted else ""

    @property
    def is_displayed(self) -> bool:
        return not self.is_shadowed and self.is_display_word and (self.is_perfect_match or not self.word_viewmodel().has_perfect_match)

    def __repr__(self) -> str:
        return (
            SkipFalsyValuesDebugReprBuilder()
            .include(self.parsed_form)
            .flag("shadowed", self.is_shadowed)
            .flag("is_display_word", self.is_display_word)
            .flag("displayed", self.is_displayed).repr)
