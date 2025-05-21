from __future__ import annotations

import language_services.conjugator
from ankiutils import app
from aqt import gui_hooks
from autoslot import Slots
from note.vocabulary.vocabnote import VocabNote
from sysutils import ex_str
from sysutils.ex_str import newline
from ui.note_content_building.content_renderer import PrerenderingAnswerContentRenderer


class ContextSentence(Slots):
    def __init__(self, japanese:str, english:str, audio:str) -> None:
        self.japanese = japanese
        self.english = english
        self.audio = audio.strip().replace("[sound:", "").replace("]", "")


def generate_highlighted_sentences_html_list(_vocab_note:VocabNote) -> str:
    primary_form = _vocab_note.question.without_noise_characters()
    conjugation_base_forms = language_services.conjugator.get_word_stems(primary_form)


    sentences:list[ContextSentence] = []
    if _vocab_note.context_sentences.first.japanese.get():
        sentences.append(ContextSentence(_vocab_note.context_sentences.first.japanese.get(), _vocab_note.context_sentences.first.english.get(), _vocab_note.context_sentences.first.audio.raw_walue()))

    if _vocab_note.context_sentences.second.japanese.get():
        sentences.append(ContextSentence(_vocab_note.context_sentences.second.japanese.get(), _vocab_note.context_sentences.second.english.get(), _vocab_note.context_sentences.second.audio.raw_walue()))

    if _vocab_note.context_sentences.second.japanese.get():
        sentences.append(ContextSentence(_vocab_note.context_sentences.second.japanese.get(), _vocab_note.context_sentences.third.english.get(), _vocab_note.context_sentences.third.audio.raw_walue()))

    sentences = [sent for sent in sentences if not app.col().sentences.with_question(sent.japanese)] #If we generated a real sentence for this sentence, don't show it


    def format_sentence(html_sentence: str) -> str:
        clean_sentence = ex_str.strip_html_and_bracket_markup(html_sentence)
        for base_form in conjugation_base_forms:
            if base_form in clean_sentence:
                return clean_sentence.replace(base_form, f"""<span class="vocabInContext">{base_form}</span>""")
        return clean_sentence


    return f'''
             <div id="highlightedSentencesSection" class="page_section">
                <div class="page_section_title">context sentences</div>
                <div id="highlightedSentencesList">
                    <div>
                        {newline.join([f"""
                        <div class="highlightedSentenceDiv">
                            <audio src="{_sentence.audio}"></audio><a class="play-button"></a>
                            <div class="highlightedSentence">
                                <div class="sentenceQuestion clipboard">{format_sentence(_sentence.japanese)}</div>
                                <div class="sentenceAnswer"> {_sentence.english}</div>
                            </div>
                        </div>
                        """ for _sentence in sentences])}
                    </div>
                </div>
            </div>
            ''' if sentences else ""

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {"##CONTEXT_SENTENCES##": generate_highlighted_sentences_html_list}).render)
