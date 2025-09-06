from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from aqt import gui_hooks
from note.sentences.sentencenote import SentenceNote
from sysutils import ex_str
from sysutils.ex_str import newline
from ui.web.sentence.sentence_viewmodel import SentenceAnalysisViewModel
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer
from viewmodels.kanji_list import sentence_kanji_list_viewmodel

if TYPE_CHECKING:
    from ui.web.sentence.match_viewmodel import MatchViewModel

def build_invalid_for_display_span(view_model: MatchViewModel) -> str:
    if not view_model.incorrect_reasons and not view_model.hiding_reasons and not view_model.not_shown_reasons: return ""

    incorrect_reasons = [f"""<div class="incorrect_reason">{reason}</div>""" for reason in view_model.incorrect_reasons]
    hiding_reasons = [f"""<div class="hiding_reason">{reason}</div>""" for reason in view_model.hiding_reasons]
    not_shown_reasons = [f"""<div class="not_shown_reason">{reason}</div>""" for reason in view_model.not_shown_reasons]
    return f"""<span>{newline.join(incorrect_reasons + hiding_reasons + not_shown_reasons)}</span>"""

def render_match_kanji(match: MatchViewModel) -> str:
    if not match.kanji or not app.config().show_kanji_in_sentence_breakdown.get_value():
        return ""

    viewmodel = sentence_kanji_list_viewmodel.create(match.kanji)

    return f"""
<div class="vocab_kanji_list">
{ex_str.newline.join(f'''
    <div class="kanji_item {" ".join(kanji.kanji.get_meta_tags())}">
        <div class="kanji_main">
            <span class="kanji_kanji clipboard">{kanji.question()}</span>
            <span class="kanji_answer">{kanji.answer()}</span>
            <span class="kanji_readings">{kanji.readings()}</span>
        </div>
        <div class="kanji_mnemonic">{kanji.mnemonic()}</div>
    </div>
''' for kanji in viewmodel.kanji_list)}
</div>
        """

def render_sentence_analysis(note: SentenceNote) -> str:
    sentence_analysis: SentenceAnalysisViewModel = SentenceAnalysisViewModel(note)
    html = """
    <div class="breakdown page_section">
        <div class="page_section_title">Sentence breakdown</div>
        <ul class="sentenceVocabList userExtra depth1">
    """

    for match in sentence_analysis.displayed_matches:
        html += f"""
                    <li class="sentenceVocabEntry depth1 word_priority_very_high {match.meta_tags_string}">
                        <div class="sentenceVocabEntryDiv">
                            {build_invalid_for_display_span(match)}
                            <audio src="{match.audio_path}"></audio><a class="play-button"></a>
                            <span class="vocabQuestion clipboard">{match.parsed_form}</span>
                            {f'''<span class="vocabHitForm clipboard">{match.vocab_form}</span>''' if match.display_vocab_form else ""}
                            {f'''<span class="vocabHitReadings clipboard">{match.readings}</span>''' if match.display_readings else ""}
                            {match.meta_tags_html}
                            <span class="vocabAnswer">{match.answer}</span>
                        </div>
                    </li>
                    """

        for compound_part in match.compound_parts:
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

        html += f"""
        <li class="sentenceVocabEntry depth1 word_priority_very_high {match.meta_tags_string}">
            {render_match_kanji(match)}
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
