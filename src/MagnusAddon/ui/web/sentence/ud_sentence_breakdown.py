from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from aqt import gui_hooks
from autoslot import Slots
from language_services.jamdict_ex.dict_lookup import DictLookup
from note.sentences.sentencenote import SentenceNote
from sysutils import ex_sequence, kana_utils
from sysutils.ex_str import newline
from ui.web.sentence.sentence_viewmodel import SentenceAnalysisViewModel
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from ui.web.sentence.candidate_word_viewmodel import CandidateWordViewModel
    from ui.web.sentence.display_form_viewmodel import DisplayFormViewModel


def build_exclusion_message_span(view_model: DisplayFormViewModel) -> str:
    exclusion_reasons = [f"""<div class="exclusion_reason">{reason}</div>""" for reason in view_model.exclusion_reasons]
    hiding_reasons = [f"""<div class="hiding_reason">{reason}</div>""" for reason in view_model.hiding_reasons]
    return f"""<span>{"<br>".join(exclusion_reasons + hiding_reasons)}</span>"""


def render_sentence_analysis(note: SentenceNote) -> str:
    sentence_analysis: SentenceAnalysisViewModel = SentenceAnalysisViewModel(note)
    candidate_words: list[CandidateWordViewModel] = sentence_analysis.analysis.candidate_words
    display_forms: list[DisplayFormViewModel] = ex_sequence.flatten([cand.display_forms for cand in candidate_words])
    displayed_forms: list[DisplayFormViewModel] = [display_form for display_form in display_forms
                                                   if display_form.is_displayed]
    html = """
    <div class="breakdown page_section">
        <div class="page_section_title">Sentence breakdown</div>
        <ul class="sentenceVocabList userExtra depth1">
    """

    for display_form in displayed_forms:
        html += f"""
                    <li class="sentenceVocabEntry depth1 word_priority_very_high {display_form.meta_tags}">
                        <div class="sentenceVocabEntryDiv">
                            {build_exclusion_message_span(display_form) if display_form.should_be_excluded else ""}
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
                        <li class="sentenceVocabEntry compound_part {compound_part.meta_tags}">
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


def _build_vocab_list(word_to_show: list[str], excluded_words: set[str], title: str, include_mnemonics: bool = False,
                      show_words_missing_dictionary_entries: bool = False,
                      include_extended_sentence_statistics: bool = False) -> str:
    html = f"""
    <div class="breakdown page_section">
        <div class="page_section_title">{title}</div>
        <ul class="sentenceVocabList userExtra depth1">
"""
    for word in (w for w in word_to_show if w not in excluded_words):
        vocabs = lookup_vocabs(excluded_words, word)

        if vocabs:
            for vocab in vocabs:
                word_form = vocab.get_question() if vocab.matching_rules.question_overrides_form.is_set() else word
                hit_form = vocab.get_question() if vocab.get_question() != word_form else ""
                needs_reading = kana_utils.contains_kanji(word_form) and (
                        not hit_form or kana_utils.contains_kanji(hit_form))
                readings = ", ".join(vocab.readings.get()) if needs_reading else ""
                html += f"""
                    <li class="sentenceVocabEntry depth1 word_priority_very_high {" ".join(vocab.get_meta_tags())}">
                        <div class="sentenceVocabEntryDiv">
                            <audio src="{vocab.audio.get_primary_audio_path()}"></audio><a class="play-button"></a>
                            <span class="vocabQuestion clipboard">{word_form}</span>
                            {f'''<span class="vocabHitForm clipboard">{hit_form}</span>''' if hit_form else ""}
                            {f'''<span class="vocabHitReadings clipboard">{readings}</span>''' if readings else ""}
                            {vocab.meta_data.meta_tags_html(include_extended_sentence_statistics)}
                            <span class="vocabAnswer">{vocab.get_answer()}</span>
                        </div>
                        {f'''<div class="sentenceVocabEntryMnemonic">{vocab.user.mnemonic.get()}</div>''' if include_mnemonics and vocab.user.mnemonic.get() and vocab.user.mnemonic.get() != '-' else ''}
                    </li>
                        """
        else:
            class Hit(Slots):
                def __init__(self, forms: str, readings_: str, answer: str) -> None:
                    self.forms: str = forms
                    self.readings: str = readings_
                    self.answer = answer

            dictionary_hits = [
                Hit(forms=",".join(hit.valid_forms()), readings_=",".join(f.text for f in hit.entry.kana_forms),
                    answer=hit.generate_answer()) for hit in DictLookup.lookup_word(word).entries]

            if not dictionary_hits and show_words_missing_dictionary_entries:
                dictionary_hits = [Hit(word, "", "---")]

            html += newline.join(f"""
                        <li class="sentenceVocabEntry depth1 word_priority_very_low">
                            <div class="sentenceVocabEntryDiv">
                                <span class="vocabQuestion clipboard">{word}</span>
                                {f'''<span class="vocabHitForm clipboard">{hit.forms}</span>''' if hit.forms != word else ""}
                                <span class="vocabHitReadings clipboard">{hit.readings}</span>
                                <span class="vocabAnswer">{hit.answer}</span>
                            </div>
                        </li>
""" for hit in dictionary_hits)

    html += """</ul>
        </div>
    """
    return html


def lookup_vocabs(excluded_words: set[str], word: str) -> list[VocabNote]:
    vocabs: list[VocabNote] = app.col().vocab.with_form(word)
    vocabs = [voc for voc in vocabs if voc.get_question() not in excluded_words]
    exact_match = [voc for voc in vocabs if voc.question.without_noise_characters() == word]
    if exact_match:
        vocabs = exact_match
    return vocabs


def render_incorrect_matches(note: SentenceNote) -> str:
    excluded_words = {x.word for x in note.configuration.incorrect_matches.get()}
    excluded_vocab = list(excluded_words)
    return _build_vocab_list(excluded_vocab, set(), "incorrectly matched words",
                             show_words_missing_dictionary_entries=True) if excluded_vocab else ""


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, {
        "##SENTENCE_ANALYSIS##": render_sentence_analysis,
        "##INCORRECT_MATCHES##": render_incorrect_matches
    }).render)
