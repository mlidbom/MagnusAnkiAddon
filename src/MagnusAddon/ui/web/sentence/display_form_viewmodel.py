from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
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
        self._config: SentenceConfiguration = word_viewmodel().candidate_word.candidate_word().analysis().configuration
        self.word_viewmodel: WeakRef[CandidateWordViewModel] = word_viewmodel
        self.is_shadowed: bool = word_viewmodel().is_shadowed
        self.is_display_word: bool = word_viewmodel().is_display_word
        self.parsed_form: str = display_form.parsed_form
        self.answer: str = display_form.answer
        self.vocab_form: str = display_form.vocab_form
        self.compound_parts: list[CompoundPartViewModel] = []
        self.audio_path: str = ""
        self.is_highlighted: bool = self.parsed_form in self._config.highlighted_words or self.vocab_form in self._config.highlighted_words
        self.readings: str = ", ".join(display_form.readings)
        self.meta_tags_html: str = ""
        self._meta_tags: str = ""
        self.display_vocab_form: bool = False
        self.match_owns_form: bool = self.parsed_form == self.vocab_form
        self.display_readings: bool = self.parsed_form != self.readings
        if isinstance(display_form, VocabMatch):
            self.compound_parts = CompoundPartViewModel.get_compound_parts_recursive(display_form.vocab, self._config)
            self.audio_path = display_form.vocab.audio.get_primary_audio_path()
            self._meta_tags = " ".join(display_form.vocab.get_meta_tags())
            self.meta_tags_html = display_form.vocab.meta_data.meta_tags_html(display_extended_sentence_statistics=False)
            self.match_owns_form = display_form.vocab.forms.is_owned_form(self.parsed_form)
            if self.parsed_form != self.vocab_form:
                self.display_vocab_form = True
                self.display_readings = self.vocab_form != self.readings

    @property
    def meta_tags(self) -> str:
        tags = self._meta_tags
        tags += " highlighted" if self.is_highlighted else ""
        tags += " shadowed" if self.is_shadowed else ""
        tags += " display_word" if self.is_display_word else ""
        tags += " hidden_word" if not self.is_display_word else ""
        tags += " secondary_match" if not self.is_primary_match() else ""
        tags += " primary_match" if self.is_primary_match() else ""
        return tags

    @property
    def is_displayed(self) -> bool:
        if app.config().show_all_matched_words_in_sentence_breakdown.get_value(): return True
        return not self.is_shadowed and self.is_display_word and self.is_primary_match()

    def is_primary_match(self) -> bool:
        return self.match_owns_form or not self.word_viewmodel().has_perfect_match

    def __repr__(self) -> str:
        return (
            SkipFalsyValuesDebugReprBuilder()
            .include(self.parsed_form)
            .flag("shadowed", self.is_shadowed)
            .flag("is_display_word", self.is_display_word)
            .flag("displayed", self.is_displayed).repr)
