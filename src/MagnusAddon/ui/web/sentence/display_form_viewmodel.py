from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from language_services.janome_ex.word_extraction.display_form import DictionaryDisplayForm, DisplayForm, VocabDisplayForm
from sysutils import ex_sequence, kana_utils
from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from ui.web.sentence.compound_part_viewmodel import CompoundPartViewModel

if TYPE_CHECKING:
    from note.sentences.sentence_configuration import SentenceConfiguration
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef
    from ui.web.sentence.candidate_word_viewmodel import CandidateWordViewModel


class DisplayFormViewModel:
    def __init__(self, word_viewmodel: WeakRef[CandidateWordViewModel], display_form: DisplayForm) -> None:
        self.display_form: DisplayForm = display_form
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
        self.display_readings = False
        if isinstance(display_form, VocabDisplayForm):
            self.compound_parts: list[CompoundPartViewModel] = self._get_compound_parts_recursive(display_form.vocab, self._config)
            self.audio_path = display_form.vocab.audio.get_primary_audio_path()
            self.meta_tags = " ".join(display_form.vocab.get_meta_tags())
            self.meta_tags_html = display_form.vocab.meta_data.meta_tags_html(display_extended_sentence_statistics=False)
            if self.parsed_form == self.vocab_form:
                self.display_readings = kana_utils.contains_kanji(self.parsed_form)
            else:
                self.display_vocab_form = True
                self.display_readings = kana_utils.contains_kanji(self.vocab_form)
        if isinstance(display_form, DictionaryDisplayForm):
            self.display_readings = True

        self.meta_tags += " highlighted" if self.is_highlighted else ""

    @property
    def is_displayed(self) -> bool:
        return not self.is_shadowed and self.is_display_word and (self.is_perfect_match or not self.word_viewmodel().has_perfect_match)

    @classmethod
    def _get_compound_parts_recursive(cls, vocab_note: VocabNote, config: SentenceConfiguration, depth: int = 0, visited: set = None) -> list[CompoundPartViewModel]:
        if not app.config().show_compound_parts_in_sentence_breakdown.get_value(): return []
        if visited is None: visited = set()
        if vocab_note.get_id() in visited: return []

        visited.add(vocab_note.get_id())

        compound_parts = ex_sequence.flatten([app.col().vocab.with_form_prefer_exact_match(part) for part in vocab_note.compound_parts.primary()])

        result = []

        for part in compound_parts:
            wrapper = CompoundPartViewModel(part, depth, config)
            result.append(wrapper)
            nested_parts = cls._get_compound_parts_recursive(part, config, depth + 1, visited)
            result.extend(nested_parts)

        return result

    def __repr__(self) -> str:
        return (
            SkipFalsyValuesDebugReprBuilder()
            .include(self.parsed_form)
            .flag("shadowed", self.is_shadowed)
            .flag("is_display_word", self.is_display_word)
            .flag("displayed", self.is_displayed).repr)
