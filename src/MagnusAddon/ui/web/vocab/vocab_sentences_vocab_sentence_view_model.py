from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils.typed import non_optional

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
        yields_to = [match for match in self.sentence_view_model.result.parsed_words
                     if match.is_displayed
                     and self.start_index < match.start_index <= self.end_index < match.end_index]

        return yields_to[0] if yields_to else None

    @override
    def __repr__(self) -> str: return self.match.__repr__()

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
    def primary_match(self) -> VocabSentenceMatchViewModel: return self.displayed_matches[0] if self.displayed_matches else self.matches[0]

    def format_sentence(self) -> str:
        result = self.result

        match = self.primary_match
        is_primary = "primary" if match.is_primary_form_of(self.vocab) else "secondary"
        match_class = f"{is_primary}FormMatch"

        if match.is_displayed:
            head = result.sentence[:match.start_index]
            match_range = result.sentence[match.start_index:match.end_index]
            tail = result.sentence[match.end_index:]
            return f"""{head}<span class="vocabInContext {match_class}">{match_range}</span>{tail}"""
        else:  # noqa: RET505
            covering_match = non_optional(match.shaded_by or match.yields_to)
            covering_match_class = "compound" if covering_match.vocab_id in self.vocab.related_notes.in_compound_ids else "shadingMatch"
            head = result.sentence[:min(covering_match.start_index, match.start_index)]
            shading_pre_range = result.sentence[covering_match.start_index:match.start_index]
            match_range = result.sentence[match.start_index:match.end_index]
            shading_post_range = result.sentence[match.end_index:covering_match.end_index]
            tail = result.sentence[max(covering_match.end_index, match.end_index):]
            return "".join([head,
                            f"""<span class="vocabInContext {match_class} {covering_match_class}">{shading_pre_range}</span>""",
                            f"""<span class="vocabInContext {match_class}">{match_range}</span>""",
                            f"""<span class="vocabInContext {match_class} {covering_match_class}">{shading_post_range}</span>""",
                            tail])

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
