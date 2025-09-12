from __future__ import annotations

from typing import TYPE_CHECKING

from aqt import gui_hooks
from autoslot import Slots
from note.note_constants import Tags
from note.vocabulary.vocabnote import VocabNote
from sysutils import ex_str, kana_utils
from sysutils.ex_str import newline
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer

if TYPE_CHECKING:
    from note.sentences.parsed_word import ParsedMatch
    from note.sentences.sentencenote import SentenceNote

class VocabSentenceViewModel(Slots):
    def __init__(self, _vocab_note: VocabNote, sentence_note: SentenceNote) -> None:
        self.vocab: VocabNote = _vocab_note
        self.sentence: SentenceNote = sentence_note
        self.result = sentence_note.parsing_result.get()
        self.matches = [match for match in self.result.parsed_words if match.vocab_id == _vocab_note.get_id()]
        self.displayed_matches = [match for match in self.matches if match.is_displayed]
        self.highlighted_sentences = set(_vocab_note.sentences.user_highlighted())

    def format_sentence(self) -> str:
        result = self.result
        conjugations = self.vocab.forms.conjugations

        def highlight_displayed_match(match: ParsedMatch, class_name: str) -> str:
            head = result.sentence[:match.start_index]
            hit_range = result.sentence[match.start_index:match.end_index]
            tail = result.sentence[match.end_index:]
            return f"""{head}<span class="vocabInContext {class_name}">{hit_range}</span>{tail}"""

        matches = [match for match in result.parsed_words if match.vocab_id == self.vocab.get_id()]
        displayed_matches = [match for match in matches if match.is_displayed]
        if displayed_matches:
            match = displayed_matches[0]
            if any(form for form in conjugations.secondary_forms_containing_primary_form_forms if form.startswith(match.parsed_form)):
                return highlight_displayed_match(match, "secondaryForm")
            if any(form for form in conjugations.secondary_forms_forms if form.startswith(match.parsed_form)):
                return highlight_displayed_match(match, "secondaryForm")

            return highlight_displayed_match(match, "primaryForm")

        shaded_matches = [match for match in matches if not match.is_displayed]
        first_shaded_match = shaded_matches[0]
        match_shading_our_match = [match for match in reversed(result.parsed_words) if match.is_displayed and match.start_index <= first_shaded_match.start_index][0]
        if match_shading_our_match.vocab_id in conjugations.derived_compound_ids:
            if any(form for form in conjugations.secondary_forms_derived_compounds_forms if form.startswith(match_shading_our_match.parsed_form)):
                return highlight_displayed_match(match_shading_our_match, "secondaryFormDerivedCompoundForm")
            return highlight_displayed_match(match_shading_our_match, "derivedCompoundForm")

        return highlight_displayed_match(first_shaded_match, "undisplayedMatch")

    def is_highlighted(self) -> bool: return self.sentence in self.highlighted_sentences

    def sentence_classes(self) -> str:
        classes = ""
        if self.sentence in self.highlighted_sentences: classes += "highlighted "
        classes += " ".join(self.sentence.get_meta_tags())
        return classes

    def contains_secondary_form_with_its_own_vocabulary_note(self) -> bool:
        return any(base_form for base_form in self.vocab.forms.conjugations.secondary_forms_with_their_own_vocab_forms
                   if base_form in self.result.sentence)

    def contains_primary_form(self) -> bool:
        return (not any(covering_secondary_form for covering_secondary_form
                        in self.vocab.forms.conjugations.secondary_forms_containing_primary_form_forms
                        if covering_secondary_form in self.result.sentence)
                and any(base_form for base_form
                        in self.vocab.forms.conjugations.primary_form_forms
                        if base_form in self.result.sentence))

    def contains_secondary_form(self) -> bool:
        return any(base_forms for base_forms
                   in self.vocab.forms.conjugations.secondary_forms_forms
                   if any(base_form for base_form in base_forms
                          if base_form in self.result.sentence))

    def contains_derived_compound(self) -> bool:
        return any(stem for stem in self.vocab.forms.conjugations.derived_compounds_forms
                   if stem in self.result.sentence)

def generate_sentences_list_html(_vocab_note: VocabNote) -> str:
    primary_form = _vocab_note.question.without_noise_characters
    studying_sentences = set(_vocab_note.sentences.studying())

    def sort_sentences(_sentences: list[VocabSentenceViewModel]) -> list[VocabSentenceViewModel]:
        is_low_reliability_matching = kana_utils.is_only_kana(primary_form) and len(primary_form) <= 2

        def prefer_highlighted_for_low_reliability_matches(_sentence: VocabSentenceViewModel) -> int: return 0 if is_low_reliability_matching and _sentence.is_highlighted() else 1
        def prefer_highlighted(_sentence: VocabSentenceViewModel) -> int: return 0 if _sentence.is_highlighted() else 1
        def prefer_studying_read(_sentence: VocabSentenceViewModel) -> int: return 0 if _sentence.sentence.is_studying_read() else 1
        def prefer_studying_listening(_sentence: VocabSentenceViewModel) -> int: return 0 if _sentence.sentence.is_studying_listening() else 1
        def dislike_secondary_form_with_vocab(_sentence: VocabSentenceViewModel) -> int: return 1 if not _sentence.contains_primary_form() and _sentence.contains_secondary_form_with_its_own_vocabulary_note() else 0
        def prefer_primary_form(_sentence: VocabSentenceViewModel) -> int: return 0 if _sentence.contains_primary_form() else 1
        def dislike_tts_sentences(_sentence: VocabSentenceViewModel) -> int: return 1 if _sentence.sentence.has_tag(Tags.TTSAudio) else 0
        def prefer_short_questions(_sentence: VocabSentenceViewModel) -> int: return len(_sentence.sentence.get_question())
        def prefer_lower_priority_tag_values(_sentence: VocabSentenceViewModel) -> int: return _sentence.sentence.priority_tag_value()
        def dislike_no_translation(_sentence: VocabSentenceViewModel) -> int: return 1 if not _sentence.sentence.get_answer().strip() else 0

        def dislike_sentences_containing_secondary_form(_sentence: VocabSentenceViewModel) -> int: return 1 if _sentence.contains_secondary_form() else 0
        def dislike_contains_derived_compound(_sentence: VocabSentenceViewModel) -> int: return 1 if _sentence.contains_derived_compound() else 0

        return sorted(_sentences, key=lambda x: (dislike_secondary_form_with_vocab(x),
                                                 prefer_studying_read(x),
                                                 prefer_studying_listening(x),
                                                 prefer_highlighted_for_low_reliability_matches(x),
                                                 dislike_no_translation(x),
                                                 prefer_lower_priority_tag_values(x),
                                                 dislike_tts_sentences(x),
                                                 prefer_primary_form(x),
                                                 prefer_highlighted(x),
                                                 dislike_contains_derived_compound(x),
                                                 dislike_sentences_containing_secondary_form(x),
                                                 prefer_short_questions(x)))

    sentences = sort_sentences([VocabSentenceViewModel(_vocab_note, sentence_note) for sentence_note in _vocab_note.sentences.all()])
    primary_form_matches = len([x for x in sentences if x.contains_primary_form()])
    sentences = sentences[:30]

    return f'''
             <div id="highlightedSentencesSection" class="page_section {"" if studying_sentences else "no_studying_sentences"}">
                <div class="page_section_title" title="primary form hits: {primary_form_matches}">sentences: primary form hits: {primary_form_matches}, <span class="studing_sentence_count">studying: {len(studying_sentences)}</span></div>
                <div id="highlightedSentencesList">
                    <div>
                        {newline.join([f"""
                        <div class="highlightedSentenceDiv {_sentence.sentence_classes()}">
                            <audio src="{_sentence.sentence.audio.first_audiofile_path()}"></audio><a class="play-button"></a>
                            <div class="highlightedSentence">
                                <div class="sentenceQuestion"><span class="clipboard">{_sentence.format_sentence()}</span> <span class="deck_indicator">{_sentence.sentence.get_source_tag()}</div>
                                <div class="sentenceAnswer"> {_sentence.sentence.get_answer()}</span></div>
                            </div>
                        </div>
                        """ for _sentence in sentences])}
                    </div>
                </div>
            </div>
            ''' if sentences else ""

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {"##HIGHLIGHTED_SENTENCES##": generate_sentences_list_html}).render)
