from __future__ import annotations

from typing import TYPE_CHECKING

from aqt import gui_hooks
from note.sentences.sentencenote import SentenceNote
from sysutils.ex_str import newline
from ui.web.sentence.sentence_viewmodel import SentenceAnalysisViewModel
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer

if TYPE_CHECKING:
    from ui.web.sentence.match_viewmodel import MatchViewModel

def build_invalid_for_display_span(view_model: MatchViewModel) -> str:
    incorrect_reasons = [f"""<div class="incorrect_reason">{reason}</div>""" for reason in view_model.incorrect_reasons]
    hiding_reasons = [f"""<div class="hiding_reason">{reason}</div>""" for reason in view_model.hiding_reasons]
    not_shown_reasons = [f"""<div class="not_shown_reason">{reason}</div>""" for reason in view_model.not_shown_reasons]
    return f"""<span>{newline.join(incorrect_reasons + hiding_reasons + not_shown_reasons)}</span>"""

def render_sentence_analysis(note: SentenceNote) -> str:
    sentence_analysis: SentenceAnalysisViewModel = SentenceAnalysisViewModel(note)
    html = """
    <div class="breakdown page_section">
        <div class="page_section_title">Sentence breakdown</div>
        <ul class="sentenceVocabList userExtra depth1">
    """

    for display_form in sentence_analysis.displayed_matches:
        html += f"""
                    <li class="sentenceVocabEntry depth1 word_priority_very_high {display_form.meta_tags_string}">
                        <div class="sentenceVocabEntryDiv">
                            {build_invalid_for_display_span(display_form) if display_form.not_valid_for_display else ""}
                            <audio src="{display_form.audio_path}"></audio><a class="play-button"></a>
                            <span class="vocabQuestion clipboard">{display_form.parsed_form}</span>
                            {f'''<span class="vocabHitForm clipboard">{display_form.vocab_form}</span>''' if display_form.display_vocab_form else ""}
                            {f'''<span class="vocabHitReadings clipboard">{display_form.readings}</span>''' if display_form.display_readings else ""}
                            {display_form.meta_tags_html}
                            <span class="vocabAnswer">{display_form.answer}</span>
                        </div>
                    </li>
                    """

        for compound_part in display_form.compound_parts:
            html += f"""
                        <li class="sentenceVocabEntry compound_part {compound_part.meta_tags_string}">
                            <div class="sentenceVocabEntryDiv">
                                <audio src="{compound_part.audio_path}"></audio><a class="play-button"></a>
                                <span class="vocabQuestion clipboard">{compound_part.question}</span>
                                {f'''<span class="vocabHitReadings clipboard">{compound_part.readings}</span>''' if compound_part.display_readings else ""}
                                {compound_part.meta_tags_html}
                                <span class="vocabAnswer">{compound_part.answer}</span>
                            </div>
                        </li>
                        """

    html += """</ul>
            </div>
        """
    return html

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, {
        "##SENTENCE_ANALYSIS##": render_sentence_analysis
    }).render)
