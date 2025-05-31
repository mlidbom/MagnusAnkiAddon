from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from language_services.janome_ex.word_extraction.display_form import VocabDisplayForm
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from sysutils import ex_sequence
from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.display_form import DisplayForm
    from note.sentences.sentencenote import SentenceNote
    from note.vocabulary.vocabnote import VocabNote

class CompoundPartViewModel:
    def __init__(self, vocab_note: VocabNote, depth: int = 0) -> None:
        self.vocab_note = vocab_note
        self.depth = depth
        self.question = vocab_note.get_question()
        self.answer = vocab_note.get_answer()
        self.readings = vocab_note.readings.get()

class DisplayFormViewModel:
    def __init__(self, word_viewmodel: CandidateWordViewModel, display_form: DisplayForm) -> None:
        self.display_form: DisplayForm = display_form
        self.is_shadowed: bool = word_viewmodel.is_shadowed
        self.is_display_word = word_viewmodel.is_display_word
        self.is_displayed = not self.is_shadowed and self.is_display_word
        self.parsed_form = display_form.parsed_form
        self.answer = display_form.answer
        self.vocab_form = display_form.vocab_form
        self.compound_parts: list[CompoundPartViewModel] = []
        self.question = self.parsed_form
        self.audio_path = ""
        self.readings: str = ""
        self.meta_tags_html = ""
        self.meta_tags: str = ""
        if isinstance(display_form, VocabDisplayForm):
            self.compound_parts = self._get_compound_parts_recursive(display_form.vocab)
            self.audio_path = display_form.vocab.audio.get_primary_audio_path()
            self.readings = ", ".join(display_form.vocab.readings.get())
            self.meta_tags = " ".join(display_form.vocab.get_meta_tags())
            self.meta_tags_html = display_form.vocab.meta_data.meta_tags_html(display_extended_sentence_statistics=False)
            if self.parsed_form == self.vocab_form:
                self.parsed_form = ""
                self.readings = ""

    @classmethod
    def _get_compound_parts_recursive(cls, vocab_note: VocabNote, depth: int = 0, visited: set = None) -> list[CompoundPartViewModel]:
        if visited is None: visited = set()
        if vocab_note.get_id() in visited: return []

        visited.add(vocab_note.get_id())

        compound_parts = ex_sequence.flatten([app.col().vocab.with_form_prefer_exact_match(part) for part in vocab_note.compound_parts.primary()])

        result = []

        for part in compound_parts:
            wrapper = CompoundPartViewModel(part, depth)
            result.append(wrapper)
            nested_parts = cls._get_compound_parts_recursive(part, depth + 1, visited)
            result.extend(nested_parts)

        return result

    def __repr__(self) -> str: return (
        SkipFalsyValuesDebugReprBuilder()
        .include(self.question)
        .flag("shadowed", self.is_shadowed)
        .flag("is_display_word", self.is_display_word)
        .flag("displayed", self.is_displayed).repr)

class CandidateWordViewModel:
    def __init__(self, candidate_word: CandidateWord) -> None:
        self.candidate_word: CandidateWord = candidate_word
        self.is_shadowed: bool = candidate_word.is_shadowed
        self.is_display_word:bool = candidate_word in candidate_word.token_range().analysis().display_words
        self.display_forms: list[DisplayFormViewModel] = [DisplayFormViewModel(self, form) for form in candidate_word.display_forms]

    def __repr__(self) -> str: return (
        SkipFalsyValuesDebugReprBuilder()
        .include(self.candidate_word.form)
        .flag("display_word", self.is_display_word)
        .flag("shadowed", self.is_shadowed).repr)

class TextAnalysisViewModel(Slots):
    def __init__(self, text_analysis: TextAnalysis) -> None:
        self.analysis: TextAnalysis = text_analysis
        self.candidate_words: list[CandidateWordViewModel] = [CandidateWordViewModel(candidate_word) for candidate_word in text_analysis.all_words]

class SentenceAnalysisViewModel(Slots):
    def __init__(self, sentence: SentenceNote) -> None:
        self.sentence: SentenceNote = sentence
        self.analysis:TextAnalysisViewModel = TextAnalysisViewModel(TextAnalysis(sentence.get_question(), sentence.configuration.configuration))
