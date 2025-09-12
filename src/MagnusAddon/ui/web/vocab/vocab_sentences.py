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


def generate_sentences_list_html(_vocab_note: VocabNote) -> str:
    primary_form = _vocab_note.question.without_noise_characters
    conjugations = _vocab_note.forms.conjugations

    def contains_primary_form(_sentence: SentenceNote) -> bool:
        clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())

        return (not any(covering_secondary_form for covering_secondary_form in conjugations.secondary_forms_containing_primary_form_forms if covering_secondary_form in clean_sentence)
                and any(base_form for base_form in conjugations.primary_form_forms if base_form in clean_sentence))

    def contains_secondary_form_with_its_own_vocabulary_note(_sentence: SentenceNote) -> bool:
        clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())
        return any(base_form for base_form in conjugations.secondary_forms_with_their_own_vocab_forms if base_form in clean_sentence)

    def format_sentence_new(sentence_note: SentenceNote) -> str:
        result = sentence_note.parsing_result.get()

        def highlight_displayed_match(match: ParsedMatch, class_name: str) -> str:
            head = result.sentence[:match.start_index]
            hit_range = result.sentence[match.start_index:match.end_index]
            tail = result.sentence[match.end_index:]
            return f"""{head}<span class="vocabInContext {class_name}">{hit_range}</span>{tail}"""

        matches = [match for match in result.parsed_words if match.vocab_id == _vocab_note.get_id()]
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

    highlighted_sentences = set(_vocab_note.sentences.user_highlighted())
    studying_sentences = set(_vocab_note.sentences.studying())

    def sort_sentences(_sentences: list[SentenceNote]) -> list[SentenceNote]:
        is_low_reliability_matching = kana_utils.is_only_kana(primary_form) and len(primary_form) <= 2

        def prefer_highlighted_for_low_reliability_matches(_sentence: SentenceNote) -> int: return 0 if is_low_reliability_matching and _sentence in highlighted_sentences else 1
        def prefer_highlighted(_sentence: SentenceNote) -> int: return 0 if _sentence in highlighted_sentences else 1
        def prefer_studying_read(_sentence: SentenceNote) -> int: return 0 if _sentence.is_studying_read() else 1
        def prefer_studying_listening(_sentence: SentenceNote) -> int: return 0 if _sentence.is_studying_listening() else 1
        def dislike_secondary_form_with_vocab(_sentence: SentenceNote) -> int: return 1 if not contains_primary_form(_sentence) and contains_secondary_form_with_its_own_vocabulary_note(_sentence) else 0
        def prefer_primary_form(_sentence: SentenceNote) -> int: return 0 if contains_primary_form(_sentence) else 1
        def dislike_tts_sentences(_sentence: SentenceNote) -> int: return 1 if _sentence.has_tag(Tags.TTSAudio) else 0
        def prefer_short_questions(_sentence: SentenceNote) -> int: return len(_sentence.get_question())
        def prefer_lower_priority_tag_values(_sentence: SentenceNote) -> int: return _sentence.priority_tag_value()
        def dislike_no_translation(_sentence: SentenceNote) -> int: return 1 if not _sentence.get_answer().strip() else 0

        def dislike_sentences_containing_secondary_form(_sentence: SentenceNote) -> int:
            clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())
            return 1 if any(base_forms for base_forms in conjugations.secondary_forms_forms if any(base_form for base_form in base_forms if base_form in clean_sentence)) else 0

        def dislike_contains_derived_compound(_sentence: SentenceNote) -> int:
            clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())
            return 1 if any(stem for stem in conjugations.derived_compounds_forms if stem in clean_sentence) else 0

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

    def sentence_classes(sentence: SentenceNote) -> str:
        classes = ""
        if sentence in highlighted_sentences: classes += "highlighted "
        classes += " ".join(sentence.get_meta_tags())
        return classes

    sentences = sort_sentences(_vocab_note.sentences.all())
    primary_form_matches = len([x for x in sentences if contains_primary_form(x)])
    sentences = sentences[:30]

    return f'''
             <div id="highlightedSentencesSection" class="page_section {"" if studying_sentences else "no_studying_sentences"}">
                <div class="page_section_title" title="primary form hits: {primary_form_matches}">sentences: primary form hits: {primary_form_matches}, <span class="studing_sentence_count">studying: {len(studying_sentences)}</span></div>
                <div id="highlightedSentencesList">
                    <div>
                        {newline.join([f"""
                        <div class="highlightedSentenceDiv {sentence_classes(_sentence)}">
                            <audio src="{_sentence.audio.first_audiofile_path()}"></audio><a class="play-button"></a>
                            <div class="highlightedSentence">
                                <div class="sentenceQuestion"><span class="clipboard">{format_sentence_new(_sentence)}</span> <span class="deck_indicator">{_sentence.get_source_tag()}</div>
                                <div class="sentenceAnswer"> {_sentence.get_answer()}</span></div>
                            </div>
                        </div>
                        """ for _sentence in sentences])}
                    </div>
                </div>
            </div>
            ''' if sentences else ""

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {"##HIGHLIGHTED_SENTENCES##": generate_sentences_list_html}).render)
