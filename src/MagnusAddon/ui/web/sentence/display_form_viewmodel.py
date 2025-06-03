from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from language_services.janome_ex.word_extraction.vocab_match import VocabMatch
from sysutils import typed
from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from sysutils.simple_string_builder import SimpleStringBuilder
from ui.web.sentence.compound_part_viewmodel import CompoundPartViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.match import Match
    from note.sentences.sentence_configuration import SentenceConfiguration
    from sysutils.weak_ref import WeakRef
    from ui.web.sentence.candidate_word_viewmodel import CandidateWordViewModel

class DisplayFormViewModel:
    def __init__(self, word_viewmodel: WeakRef[CandidateWordViewModel], display_form: Match) -> None:
        self.match: Match = display_form
        self.vocab_match: VocabMatch | None = typed.try_cast(VocabMatch, display_form)
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
        if self.vocab_match is not None:
            self.compound_parts = CompoundPartViewModel.get_compound_parts_recursive(self.vocab_match.vocab, self._config)
            self.audio_path = self.vocab_match.vocab.audio.get_primary_audio_path()
            self._meta_tags = " ".join(self.vocab_match.vocab.get_meta_tags())
            self.meta_tags_html = self.vocab_match.vocab.meta_data.meta_tags_html(display_extended_sentence_statistics=False)
            self.match_owns_form = self.vocab_match.vocab.forms.is_owned_form(self.parsed_form)
            if self.parsed_form != self.vocab_form:
                self.display_vocab_form = True
                self.display_readings = self.display_readings and self.vocab_form != self.readings

    @property
    def meta_tags(self) -> str:
        tags = self._meta_tags
        tags += " highlighted" if self.is_highlighted else ""
        tags += " " + self.exclusion_reason_tags

        return tags

    @property
    def exclusion_reason_tags(self) -> str:
        return (SimpleStringBuilder(auto_separator=" ")
                .append("")
                .append_if(self.match.is_configured_hidden, "configured_hidden")
                .append_if(self.match.is_configured_incorrect, "configured_incorrect_match",)
                .append(" ".join(self.vocab_match.failure_reasons()) if self.vocab_match is not None else "")
                .append_if(self.is_shadowed, "shadowed")
                .append_if(not self.is_primary_match()).build(), "secondary_match")

    @property
    def is_displayed(self) -> bool:
        if app.config().show_all_matched_words_in_sentence_breakdown.get_value(): return True
        return (not self.is_shadowed
                and self.is_display_word
                and self.is_primary_match()
                and (self.vocab_match is None
                     or self.vocab_match.is_valid
                     or (not self.word_viewmodel().candidate_word.candidate_word().is_custom_compound
                         and len(self.word_viewmodel().display_forms) == 1))  # we are the only match for a non-compound and we have to display something
                )

    @property
    def should_be_excluded(self) -> bool:
        return (self.is_shadowed
                or self.match.is_configured_hidden
                or self.match.is_configured_incorrect
                or self.match.is_configured_hidden
                or not self.is_primary_match()
                or not self.is_display_word)

    def is_primary_match(self) -> bool:
        return self.match_owns_form or not self.word_viewmodel().has_perfect_match

    def __repr__(self) -> str:
        return (
            SkipFalsyValuesDebugReprBuilder()
            .include(self.parsed_form)
            .flag("shadowed", self.is_shadowed)
            .flag("is_display_word", self.is_display_word)
            .flag("displayed", self.is_displayed).repr)
