from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

if TYPE_CHECKING:
    from note.sentences.parsed_word import ParsedMatch
    from note.sentences.parsing_result import ParsingResult
    from note.sentences.sentencenote import SentenceNote
    from note.vocabulary.vocabnote import VocabNote

class VocabSentenceMatchViewModel(Slots):
    def __init__(self, match: ParsedMatch, sentence_view_model: VocabSentenceViewModel) -> None:
        self.match: ParsedMatch = match
        self.sentence_view_model: VocabSentenceViewModel = sentence_view_model

    @property
    def is_displayed(self) -> bool: return self.match.is_displayed
    @property
    def start_index(self) -> int: return self.match.start_index
    @property
    def end_index(self) -> int: return self.match.end_index
    def is_primary_form_of(self, vocab: VocabNote) -> bool: return self.match.parsed_form == vocab.question.without_noise_characters
    @property
    def shaded_by(self) -> ParsedMatch: return [match for match in reversed(self.sentence_view_model.result.parsed_words)
                                                if match.is_displayed and match.start_index <= self.start_index][0]

class VocabSentenceViewModel(Slots):
    def __init__(self, _vocab_note: VocabNote, sentence_note: SentenceNote) -> None:
        self.vocab: VocabNote = _vocab_note
        self.sentence: SentenceNote = sentence_note
        self.result: ParsingResult = sentence_note.parsing_result.get()
        self.matches: list[VocabSentenceMatchViewModel] = [VocabSentenceMatchViewModel(match, self) for match in self.result.parsed_words if match.vocab_id == _vocab_note.get_id()]
        self.displayed_matches: list[VocabSentenceMatchViewModel] = [match for match in self.matches if match.is_displayed]
        self.highlighted_sentences: set[SentenceNote] = set(_vocab_note.sentences.user_highlighted())
        self.shaded_matches: list[VocabSentenceMatchViewModel] = [match for match in self.matches if not match.is_displayed]

    @property
    def first_shaded_match(self) -> VocabSentenceMatchViewModel: return self.shaded_matches[0]

    @property
    def first_match(self) -> VocabSentenceMatchViewModel: return self.matches[0]

    def format_sentence(self) -> str:
        result = self.result
        conjugations = self.vocab.forms.conjugations

        def highlight_displayed_match(match: VocabSentenceMatchViewModel, class_name: str) -> str:
            head = result.sentence[:match.start_index]
            hit_range = result.sentence[match.start_index:match.end_index]
            tail = result.sentence[match.end_index:]
            return f"""{head}<span class="vocabInContext {class_name}">{hit_range}</span>{tail}"""

        def highlight_shaded_match(match: VocabSentenceMatchViewModel, shaded_by: ParsedMatch, inner_class_name: str, outer_class_name: str) -> str:
            outer_head = result.sentence[:shaded_by.start_index]
            outer_range = result.sentence[shaded_by.start_index:match.start_index]
            outer_tail = result.sentence[shaded_by.end_index:]
            inner_range = result.sentence[match.start_index:match.end_index]
            formatted_match = f"""<span class="vocabInContext {inner_class_name}">{inner_range}</span>"""
            return f"""{outer_head}<span class="vocabInContext {outer_class_name}">{outer_range}{formatted_match}</span>{outer_tail}"""

        if self.first_match.is_displayed:
            return highlight_displayed_match(self.first_match, "primaryForm" if self.first_match.is_primary_form_of(self.vocab) else "secondaryForm")

        match_shading_our_match = self.first_match.shaded_by
        if match_shading_our_match.vocab_id in conjugations.derived_compound_ids:
            if any(form for form in conjugations.secondary_forms_derived_compounds_forms if form.startswith(match_shading_our_match.parsed_form)):
                return highlight_shaded_match(self.first_match, match_shading_our_match, "secondaryForm", "secondaryFormDerivedCompoundForm")
            return highlight_shaded_match(self.first_match, match_shading_our_match, "primaryForm", "derivedCompoundForm")

        return highlight_displayed_match(self.first_shaded_match, "undisplayedMatch")

    def is_highlighted(self) -> bool: return self.sentence in self.highlighted_sentences

    @property
    def vocab_is_displayed(self) -> bool: return any(self.displayed_matches)

    def sentence_classes(self) -> str:
        classes = ""
        if self.sentence in self.highlighted_sentences: classes += "highlighted "
        classes += " ".join(self.sentence.get_meta_tags())
        return classes

    def contains_secondary_form_with_its_own_vocabulary_note(self) -> bool:
        return any(base_form for base_form in self.vocab.forms.conjugations.secondary_forms_with_their_own_vocab_forms
                   if base_form in self.result.sentence)

    def contains_primary_form(self) -> bool:
        return any(match for match in self.displayed_matches if match.is_primary_form_of(self.vocab))

    def contains_secondary_form(self) -> bool:
        return any(base_forms for base_forms
                   in self.vocab.forms.conjugations.secondary_forms_forms
                   if any(base_form for base_form in base_forms
                          if base_form in self.result.sentence))

    def contains_derived_compound(self) -> bool:
        return any(stem for stem in self.vocab.forms.conjugations.derived_compounds_forms
                   if stem in self.result.sentence)
