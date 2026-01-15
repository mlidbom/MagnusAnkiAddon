from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from aqt import gui_hooks
from configuration.settings import Settings
from note.sentences.sentencenote import SentenceNote
from sysutils import ex_str
from sysutils.ex_str import newline
from ui.web.sentence.sentence_viewmodel import SentenceViewModel
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer
from viewmodels.kanji_list import sentence_kanji_list_viewmodel

if TYPE_CHECKING:
    from collections.abc import Callable

    from configuration.configuration_value import ConfigurationValueBool
    from language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
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
        "hide_all_compounds": "HAC"
}

def render_view_settings() -> str:
    def get_toggle_abbreviation(toggle: str) -> str:
        return _toggle_abbreviations.get(toggle, f"MISSING_ABBREVIATION:{toggle}")

    def render_toggle(toggle: ConfigurationValueBool) -> str:
        return f"""<span class="toggle {toggle.name}" title="{toggle.title}">{get_toggle_abbreviation(toggle.name)}</span>  """

    def render_toggle_list() -> str:
        return newline.join(render_toggle(toggle) for toggle in app.config().sentence_view_toggles if toggle.get_value())

    return f"""
    <span class="view_settings">
        <span class="view_settings_title">Settings:</span>
        {render_toggle_list()}
    </span>
"""

def render_sentence_analysis(note: SentenceNote) -> str:
    sentence_analysis: SentenceViewModel = SentenceViewModel(note)
    html = f"""
    <div class="breakdown page_section">
        <div class="page_section_title">Sentence breakdown  #  {render_view_settings()}</div>
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

    html += render_tokens(sentence_analysis)

    return html

_token_boolean_flags: list[tuple[Callable[[IAnalysisToken], bool], str, str]] = [
        (lambda t: t.is_past_tense_stem, "PTS", "past_tense_stem"),
        (lambda t: t.is_past_tense_marker, "PTM", "past_tense_marker"),
        (lambda t: t.is_masu_stem, "Masu", "masu_stem"),
        (lambda t: t.is_adverb, "Adv", "adverb"),
        (lambda t: t.is_irrealis, "Irr", "irrealis"),
        (lambda t: t.is_end_of_statement, "EOS", "end_of_statement"),
        (lambda t: t.has_te_form_stem, "HTFS", "has_te_form_stem"),
        (lambda t: t.is_non_word_character, "NWC", "non_word_character"),
        (lambda t: t.is_dictionary_verb_form_stem, "DVS", "dictionary_verb_form_stem"),
        (lambda t: t.is_dictionary_verb_inflection, "DVI", "dictionary_verb_inflection"),
        (lambda t: t.is_godan_potential_stem, "GPS", "godan_potential_stem"),
        (lambda t: t.is_godan_imperative_stem, "GIS", "godan_imperative_stem"),
        (lambda t: t.is_ichidan_imperative_stem, "IIS", "ichidan_imperative_stem"),
        (lambda t: t.is_godan_potential_inflection, "GPI", "godan_potential_inflection"),
        (lambda t: t.is_godan_imperative_inflection, "GII", "godan_imperative_inflection"),
        (lambda t: t.is_ichidan_imperative_inflection, "III", "ichidan_imperative_inflection"),
        (lambda t: t.is_inflectable_word, "Infl", "inflectable_word"),
        (lambda t: t.is_ichidan_verb, "一段", "ichidan_verb"),
        (lambda t: t.is_godan_verb, "五弾", "godan_verb"),
]
def render_tokens(sentence_analysis: SentenceViewModel) -> str:
    if not Settings.show_breakdown_in_edit_mode(): return ""

    tokens: list[IAnalysisToken] = sentence_analysis.analysis.analysis.pre_processed_tokens

    def render_token_properties(token: IAnalysisToken) -> str:
        properties: list[str] = []
        for prop_func, _, title in _token_boolean_flags:
            if prop_func(token):
                properties.append(f'<span class="token_property" title="{title}">{title}</span>')

        return ", ".join(properties) if properties else ""

    html = """
    <div class="tokens page_section">
        <div class="page_section_title">Tokens</div>
        <table>
            <thead>
                <tr>
                    <th>Surface</th>
                    <th>Base</th>
                    <th>Boolean flags</th>
                    <th>Token class</th>
                    <th title="Parts of speech">POS1</th>
                    <th title="Parts of speech">POS2</th>
                    <th title="Parts of speech">POS3</th>
                    <th title="Parts of speech">POS4</th>
                    <th title="Inflected form">Inflected Form</th>
                    <th title="Inflection type">Inflection Type</th>
                </tr>
            </thead>
            <tbody>
"""

    for token in tokens:
        html += f"""
                    <tr>
                        <td class="surface"><span class="japanese clipboard">{token.surface}</span></td>
                        <td class="base"><span class="japanese clipboard">{token.base_form}</span></td>
                        <td class="token_properties">{render_token_properties(token)}</td>
                        <td class="token_properties">{token.__class__.__name__}</td>
                        <td class="pos pos1"><span class="japanese clipboard">{token.source_token.parts_of_speech.level1.japanese}</span>:{token.source_token.parts_of_speech.level1.english}</td>
                        <td class="pos pos2"><span class="japanese clipboard">{token.source_token.parts_of_speech.level2.japanese}</span>:{token.source_token.parts_of_speech.level2.english}</td>
                        <td class="pos pos3"><span class="japanese clipboard">{token.source_token.parts_of_speech.level3.japanese}</span>:{token.source_token.parts_of_speech.level3.english}</td>
                        <td class="pos pos4"><span class="japanese clipboard">{token.source_token.parts_of_speech.level4.japanese}</span>:{token.source_token.parts_of_speech.level4.english}</td>
                        <td class="inflected_form clipboard">{token.source_token.inflected_form}</td>
                        <td class="inflection_type clipboard">{token.source_token.inflection_type}</td>
                    </tr>
                """

    html += """
            </tbody>
        </table>
    </div>
"""
    return html

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, {
            "##SENTENCE_ANALYSIS##": render_sentence_analysis
    }).render)
