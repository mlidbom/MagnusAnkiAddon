from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from aqt import gui_hooks
from autoslot import Slots
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from note.sentences.sentencenote import SentenceNote
from sysutils import kana_utils
from sysutils.ex_str import newline
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote


def _build_vocab_list(word_to_show: list[str], excluded_words:set[str], title:str, include_mnemonics:bool = False, show_words_missing_dictionary_entries:bool = False, include_extended_sentence_statistics:bool = False) -> str:
    html = f"""
    <div class="breakdown page_section">
        <div class="page_section_title">{title}</div>
        <ul class="sentenceVocabList userExtra depth1">
"""
    for word in (w for w in word_to_show if w not in excluded_words):
        vocabs = lookup_vocabs(excluded_words, word)

        if vocabs:
            for vocab in vocabs:
                word_form = vocab.get_question() if vocab.meta_data.flags.question_overrides_form() else word
                hit_form = vocab.get_question() if vocab.get_question() != word_form else ""
                needs_reading = kana_utils.contains_kanji(word_form) and (not hit_form or kana_utils.contains_kanji(hit_form))
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
                            {f'''<div class="sentenceVocabEntryMnemonic">{vocab.user.mnemonic.get()}</div>''' if include_mnemonics and vocab.user.mnemonic.get() and vocab.user.mnemonic.get() != '-' else '' }
                        </li>
                        """
        else:
            class Hit(Slots):
                def __init__(self, forms:str, readings_:str, answer:str) -> None:
                    self.forms: str = forms
                    self.readings: str = readings_
                    self.answer = answer

            dictionary_hits = [Hit(forms=",".join(hit.valid_forms()), readings_=",".join(f.text for f in hit.entry.kana_forms), answer=hit.generate_answer()) for hit in DictLookup.lookup_word(word).entries]

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

def lookup_vocabs(excluded_words: set[str], word:str) -> list[VocabNote]:
    vocabs: list[VocabNote] = app.col().vocab.with_form(word)
    vocabs = [voc for voc in vocabs if voc.get_question() not in excluded_words]
    exact_match = [voc for voc in vocabs if voc.question.without_noise_characters() == word]
    if exact_match:
        vocabs = exact_match
    return vocabs

def render_parsed_words(note: SentenceNote) -> str:
    analysis = TextAnalysis(note.get_question(), note.configuration.configuration)
    display_forms = analysis.display_words
    word_strings = [w.form for w in display_forms]

    excluded = note.configuration.incorrect_matches.words()
    return _build_vocab_list(word_strings, excluded, "parsed words", show_words_missing_dictionary_entries=True)

def render_incorrect_matches(note: SentenceNote) -> str:
    excluded_words = {x.word for x in note.configuration.incorrect_matches.get()}
    excluded_vocab = list(excluded_words)
    return _build_vocab_list(excluded_vocab, set(), "incorrectly matched words", show_words_missing_dictionary_entries=True) if excluded_vocab else ""

def render_hidden_matches(note: SentenceNote) -> str:
    hidden_words = {x.word for x in note.configuration.hidden_matches.get()}
    hidden_vocab = list(hidden_words)
    return _build_vocab_list(hidden_vocab, set(), "hidden words", show_words_missing_dictionary_entries=True) if hidden_vocab else ""

def render_user_extra_list(note: SentenceNote) -> str:
    return _build_vocab_list(note.configuration.highlighted_words(), note.configuration.incorrect_matches.words(), "highlighted words", include_mnemonics=True, show_words_missing_dictionary_entries=True, include_extended_sentence_statistics=True) if note.configuration.highlighted_words() else ""

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, {
        "##PARSED_WORDS##": render_parsed_words,
        "##INCORRECT_MATCHES##": render_incorrect_matches,
        "##HIDDEN_MATCHES##": render_hidden_matches,
        "##USER_EXTRA_VOCAB##": render_user_extra_list,
    }).render)
