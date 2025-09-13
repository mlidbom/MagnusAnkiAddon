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
    def shaded_by(self) -> ParsedMatch | None:
        shading = [match for match in reversed(self.sentence_view_model.result.parsed_words)
                   if match.is_displayed
                   and match.start_index <= self.start_index <= match.end_index]

        return shading[0] if shading else None

    @property
    def yields_to(self) -> ParsedMatch | None:
        shading = [match for match in self.sentence_view_model.result.parsed_words
                   if match.is_displayed
                   and self.start_index < match.start_index <= self.end_index < match.end_index]

        return shading[0] if shading else None

class VocabSentenceViewModel(Slots):
    def __init__(self, _vocab_note: VocabNote, sentence_note: SentenceNote) -> None:
        self.vocab: VocabNote = _vocab_note
        self.sentence: SentenceNote = sentence_note
        self.result: ParsingResult = sentence_note.parsing_result.get()
        self.matches: list[VocabSentenceMatchViewModel] = [VocabSentenceMatchViewModel(match, self) for match in self.result.parsed_words if match.vocab_id == _vocab_note.get_id()]
        self.displayed_matches: list[VocabSentenceMatchViewModel] = [match for match in self.matches if match.is_displayed]
        self.highlighted_sentences: set[SentenceNote] = set(_vocab_note.sentences.user_highlighted())
        self.shaded_matches: list[VocabSentenceMatchViewModel] = [match for match in self.matches if not match.is_displayed]
        self.matched_vocab_ids: set[int] = {match.vocab_id for match in self.result.parsed_words}

    @property
    def prioritized_match(self) -> VocabSentenceMatchViewModel: return self.displayed_matches[0] if self.displayed_matches else self.matches[0]

    def format_sentence(self) -> str:
        result = self.result

        def highlight_displayed_match(match: VocabSentenceMatchViewModel, class_name: str) -> str:
            head = result.sentence[:match.start_index]
            hit_range = result.sentence[match.start_index:match.end_index]
            tail = result.sentence[match.end_index:]
            return f"""{head}<span class="vocabInContext {class_name}">{hit_range}</span>{tail}"""

        def highlight_shaded_match(match: VocabSentenceMatchViewModel, shaded_by: ParsedMatch, match_class: str, shaded_by_class: str) -> str:
            if shaded_by.end_index < match.end_index:
                shading_head = result.sentence[:shaded_by.start_index]
                shading_range = result.sentence[shaded_by.start_index:match.start_index]
                match_range = result.sentence[match.start_index:match.end_index]
                tail = result.sentence[max(shaded_by.end_index, match.end_index):]
                formatted_match = f"""<span class="vocabInContext {match_class}">{match_range}</span>"""
                return f"""{shading_head}<span class="vocabInContext {shaded_by_class}">{shading_range}{formatted_match}</span>{tail}"""
            else:
                shading_head = result.sentence[:shaded_by.start_index]
                shading_pre_range = result.sentence[shaded_by.start_index:match.start_index]
                match_range = result.sentence[match.start_index:match.end_index]
                shading_post_range = result.sentence[match.end_index:shaded_by.end_index]
                tail = result.sentence[shaded_by.end_index:]
                formatted_match = f"""<span class="vocabInContext {match_class}">{match_range}</span>"""
                return f"""{shading_head}<span class="vocabInContext {shaded_by_class}">{shading_pre_range}{formatted_match}{shading_post_range}</span>{tail}"""

        def highlight_yielded_to_match(match: VocabSentenceMatchViewModel, yielded_to: ParsedMatch, yielded_to_class: str, match_class: str) -> str:
            match_head = result.sentence[:match.start_index]
            match_range = result.sentence[match.start_index:yielded_to.start_index]
            yielded_to_range = result.sentence[yielded_to.start_index:yielded_to.end_index]
            yielded_to_tail = result.sentence[yielded_to.end_index:]
            return f"""{match_head}<span class="vocabInContext {match_class}">{match_range}</span><span class="vocabInContext {yielded_to_class}">{yielded_to_range}</span>{yielded_to_tail}"""

        match_class = "primary" if self.prioritized_match.is_primary_form_of(self.vocab) else "secondary"
        if self.prioritized_match.is_displayed:
            return highlight_displayed_match(self.prioritized_match, f"{match_class}Form")

        match_yielded_to = self.prioritized_match.yields_to
        if match_yielded_to:
            return highlight_yielded_to_match(self.prioritized_match, match_yielded_to, f"{match_class}Form yieldedMatch", "yieldedToMatch")

        match_shading_our_match = self.prioritized_match.shaded_by
        if not match_shading_our_match: raise AssertionError("This should never happen")

        if match_shading_our_match.vocab_id in self.vocab.related_notes.in_compound_ids:
            return highlight_shaded_match(self.prioritized_match, match_shading_our_match, f"{match_class}Form", f"{match_class}CompoundForm")

        return highlight_shaded_match(self.prioritized_match, match_shading_our_match, f"{match_class}Form shadedMatch", "shadingMatch")

    def is_highlighted(self) -> bool: return self.sentence in self.highlighted_sentences

    @property
    def vocab_is_displayed(self) -> bool: return any(self.displayed_matches)

    def sentence_classes(self) -> str:
        classes = ""
        if self.sentence in self.highlighted_sentences: classes += "highlighted "
        classes += " ".join(self.sentence.get_meta_tags())
        return classes

    def contains_primary_form(self) -> bool:
        return any(match for match in self.displayed_matches if match.is_primary_form_of(self.vocab))
