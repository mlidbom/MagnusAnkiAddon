from __future__ import annotations

from typing import TYPE_CHECKING, override

from ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
from sysutils import kana_utils, typed
from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from sysutils.simple_string_list_builder import SimpleStringListBuilder
from typed_linq_collections.q_iterable import query
from ui.web.sentence.compound_part_viewmodel import CompoundPartViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from note.sentences.sentence_configuration import SentenceConfiguration
    from sysutils.weak_ref import WeakRef
    from ui.web.sentence.candidate_word_variant_viewmodel import CandidateWordVariantViewModel

class MatchViewModel(Slots):
    def __init__(self, word_variant_vm: WeakRef[CandidateWordVariantViewModel], match: Match) -> None:
        self.match: Match = match
        self.vocab_match: VocabMatch | None = typed.try_cast(VocabMatch, match)
        self._config: SentenceConfiguration = word_variant_vm().candidate_word.word.analysis.configuration
        self.word_variant_vm: WeakRef[CandidateWordVariantViewModel] = word_variant_vm
        self.is_display_word: bool = word_variant_vm().is_display_word
        self.parsed_form: str = match.parsed_form
        self.answer: str = match.answer
        self.vocab_form: str = match.match_form
        self.compound_parts: list[CompoundPartViewModel] = []
        self.audio_path: str = ""
        self.is_highlighted: bool = self.parsed_form in self._config.highlighted_words or self.vocab_form in self._config.highlighted_words
        self.readings: str = ", ".join(match.readings)
        self.meta_tags_html: str = ""
        self._meta_tags: list[str] = []
        self.display_vocab_form: bool = self.parsed_form != self.vocab_form
        self.match_owns_form: bool = self.parsed_form == self.vocab_form
        self.display_readings: bool = self.parsed_form != self.readings
        if self.vocab_match is not None:
            self.compound_parts = CompoundPartViewModel.get_compound_parts_recursive(self.vocab_match.vocab, self._config)
            self.audio_path = self.vocab_match.vocab.audio.get_primary_audio_path()
            self._meta_tags = list(self.vocab_match.vocab.get_meta_tags())
            self.meta_tags_html = self.vocab_match.vocab.meta_data.meta_tags_html(display_extended_sentence_statistics=False)
            self.match_owns_form = self.vocab_match.vocab.forms.is_owned_form(self.parsed_form)
            if self.parsed_form != self.vocab_form:
                self.display_vocab_form = True
                self.display_readings = self.display_readings and self.vocab_form != self.readings

    @property
    def meta_tags_string(self) -> str: return " ".join(self.meta_tags_list)

    @property
    def meta_tags_list(self) -> list[str]:
        return (SimpleStringListBuilder()
                .concat(self._meta_tags)
                .append_if(self.is_highlighted, "highlighted")
                .concat(self.hiding_reasons)
                .value)

    @property
    def incorrect_reasons(self) -> list[str]: return list(self.match.failure_reasons)

    @property
    def hiding_reasons(self) -> list[str]: return list(self.match.hiding_reasons)

    @property
    def is_displayed(self) -> bool:
        if app.config().show_sentence_breakdown_in_edit_mode.get_value(): return True
        #todo: this absolutely does not belong here. This is a viewmodel for crying out loud, it should not be implementing core domain logic.
        return (self.is_display_word
                and self.match.is_displayed)

    @property
    def kanji(self) -> list[str]:
        sequence = kana_utils.extract_kanji(self.parsed_form + self.vocab_form)
        return query(sequence).distinct().to_list()

    @override
    def __repr__(self) -> str:
        return (
            SkipFalsyValuesDebugReprBuilder()
            .include(self.parsed_form)
            .flag("is_display_word", self.is_display_word)
            .flag("displayed", self.is_displayed).repr)
