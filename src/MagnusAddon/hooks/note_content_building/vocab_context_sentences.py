from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor

from anki.cards import Card
from aqt import gui_hooks

from ankiutils import app, ui_utils
from hooks.note_content_building.content_renderer import PrerenderingAnswerSingleTagContentRenderer
from note.jpnote import JPNote
from note.vocabnote import VocabNote
from sysutils import ex_str, kana_utils
from sysutils.ex_str import newline
from sysutils.typed import checked_cast

class ContextSentence:
    def __init__(self, japanese:str, english:str, audio:str) -> None:
        self.japanese = japanese
        self.english = english
        self.audio = audio.strip().replace("[sound:", "").replace("]", "")


def generate_highlighted_sentences_html_list(_vocab_note:VocabNote) -> str:
    primary_form = _vocab_note.get_question_without_noise_characters()
    conjugation_base_form = kana_utils.get_conjugation_base(primary_form)


    sentences:list[ContextSentence] = []
    if _vocab_note.get_context_jp():
        sentences.append(ContextSentence(_vocab_note.get_context_jp(), _vocab_note.get_context_en(), _vocab_note.get_context_jp_audio()))

    if _vocab_note.get_context_jp_2():
        sentences.append(ContextSentence(_vocab_note.get_context_jp_2(), _vocab_note.get_context_en_2(), _vocab_note.get_context_jp_2_audio()))

    if _vocab_note.get_context_jp_3():
        sentences.append(ContextSentence(_vocab_note.get_context_jp_3(), _vocab_note.get_context_en_3(), _vocab_note.get_context_jp_3_audio()))

    sentences = [sent for sent in sentences if not app.col().sentences.with_question(sent.japanese)] #If we generated a real sentence for this sentence, don't show it


    def format_sentence(html_sentence: str) -> str:
        clean_sentence = ex_str.strip_html_and_bracket_markup(html_sentence)
        return clean_sentence.replace(conjugation_base_form, f"""<span class="vocabInContext">{conjugation_base_form}</span>""")


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
    gui_hooks.card_will_show.append(PrerenderingAnswerSingleTagContentRenderer(VocabNote, "##CONTEXT_SENTENCES##", generate_highlighted_sentences_html_list).render)
