from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from aqt import gui_hooks
from configuration.configuration_value import ConfigurationValueBool
from configuration.settings import Settings
from note.sentences.sentencenote import SentenceNote
from sysutils import ex_str
from sysutils.ex_str import newline
from ui.web.sentence.sentence_viewmodel import SentenceViewModel
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer
from viewmodels.kanji_list import sentence_kanji_list_viewmodel

if TYPE_CHECKING:
    from ui.web.sentence.match_viewmodel import MatchViewModel

def format_reason(reason: str) -> str:
    return f"""<span class="configured">{reason}</span>""" if "configured" in reason else reason

def build_invalid_for_display_span(view_model: MatchViewModel) -> str:
    if not Settings.show_breakdown_in_edit_mode() or (not view_model.incorrect_reasons and not view_model.hiding_reasons): return ""
    incorrect_reasons = [f"""<div class="incorrect_reason">{format_reason(reason)}</div>""" for reason in view_model.incorrect_reasons]
    hiding_reasons = [f"""<div class="hiding_reason">{format_reason(reason)}</div>""" for reason in view_model.hiding_reasons]
    return f"""<span>{newline.join(incorrect_reasons + hiding_reasons)}</span>"""

def render_match_kanji(match: MatchViewModel) -> str:
    if not match.show_kanji: return ""
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
        {f"""<div class="kanji_mnemonic">{kanji.mnemonic()}</div>""" if match.show_kanji_mnemonics else ""}
    </div>
''' for kanji in viewmodel.kanji_list)}
</div>
        """

_toggle_abbreviations: dict[str, str] = {
        "show_sentence_breakdown_in_edit_mode": "EM",
        "show_kanji_in_sentence_breakdown": "SK",
        "show_compound_parts_in_sentence_breakdown": "SCP",
        "show_kanji_mnemonics_in_sentence_breakdown": "SKM",
        "automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound": "YSV",
        "automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound": "YPV",
        "automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound": "YCV",
        "hide_compositionally_transparent_compounds": "HCTC",
        "hide_all_compounds": "HAC",

}

def render_view_settings() -> str:
    def get_toggle_abbreviation(toggle: str) -> str:
        return _toggle_abbreviations.get(toggle, f"MISSING_ABBREVIATION:{toggle}")

    def render_toggle(toggle: ConfigurationValueBool) -> str:
        return f"""<span class="toggle {toggle.name}" title="{toggle.title}">{get_toggle_abbreviation(toggle.name)}</span>  """

    def render_toggle_list() -> str:
        return newline.join(render_toggle(toggle) for toggle in app.config().sentence_view_toggles if toggle.get_value())

    return f"""
    <div class="view_settings">
        <span class="view_settings_title">Active settings:</span>
        {render_toggle_list()}
    </div>
"""

def render_sentence_analysis(note: SentenceNote) -> str:
    sentence_analysis: SentenceViewModel = SentenceViewModel(note)
    html = f"""
    <div class="breakdown page_section">
        <div class="page_section_title">Sentence breakdown</div>
        {render_view_settings()}
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

        if match.show_compound_parts:
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
