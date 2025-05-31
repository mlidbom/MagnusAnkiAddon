from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from language_services.janome_ex.word_extraction.display_form import VocabDisplayForm, DictionaryDisplayForm
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from sysutils import ex_sequence, kana_utils
from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from sysutils.weak_ref import WeakRef

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
        self.readings = ", ".join(vocab_note.readings.get())
        self.audio_path = vocab_note.audio.get_primary_audio_path()
        self.meta_tags_html = vocab_note.meta_data.meta_tags_html(display_extended_sentence_statistics=False)
        self.display_readings = kana_utils.contains_kanji(self.question)

        self.meta_tags = " ".join(vocab_note.get_meta_tags())
        self.meta_tags += f""" depth_{depth}"""


class DisplayFormViewModel:
    def __init__(self, word_viewmodel: WeakRef[CandidateWordViewModel], display_form: DisplayForm) -> None:
        self.display_form: DisplayForm = display_form
        self.word_viewmodel: WeakRef[CandidateWordViewModel] = word_viewmodel
        self.is_shadowed: bool = word_viewmodel().is_shadowed
        self.is_display_word = word_viewmodel().is_display_word
        self.parsed_form = display_form.parsed_form
        self.answer = display_form.answer
        self.vocab_form = display_form.vocab_form
        self.compound_parts: list[CompoundPartViewModel] = []
        self.audio_path = ""
        self.readings: str = ", ".join(display_form.readings)
        self.meta_tags_html = ""
        self.meta_tags: str = ""
        self.display_vocab_form = False
        self.is_perfect_match = self.parsed_form == self.vocab_form
        self.display_readings = False
        if isinstance(display_form, VocabDisplayForm):
            self.compound_parts:list[CompoundPartViewModel] = self._get_compound_parts_recursive(display_form.vocab)
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


    @property
    def is_displayed(self) -> bool:
        return not self.is_shadowed and self.is_display_word and (self.is_perfect_match or not self.word_viewmodel().has_perfect_match)

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
        .include(self.parsed_form)
        .flag("shadowed", self.is_shadowed)
        .flag("is_display_word", self.is_display_word)
        .flag("displayed", self.is_displayed).repr)

class CandidateWordViewModel:
    def __init__(self, candidate_word: CandidateWord) -> None:
        self.candidate_word: CandidateWord = candidate_word
        self.weakref:WeakRef[CandidateWordViewModel] = WeakRef(self)
        self.is_shadowed: bool = candidate_word.is_shadowed
        self.is_display_word:bool = candidate_word in candidate_word.token_range().analysis().display_words
        self.display_forms: list[DisplayFormViewModel] = [DisplayFormViewModel(self.weakref, form) for form in candidate_word.display_forms]
        self.has_perfect_match = any(form.is_perfect_match for form in self.display_forms)

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
