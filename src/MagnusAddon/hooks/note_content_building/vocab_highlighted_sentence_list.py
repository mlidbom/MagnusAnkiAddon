from anki.cards import Card
from aqt import gui_hooks

from ankiutils import ui_utils
from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_sequence, ex_str, kana_utils
from sysutils.ex_str import newline


def generate_highlighted_sentences_html_list(_vocab_note: VocabNote) -> str:
    def format_sentence(html_sentence: str) -> str:
        clean_sentence = ex_str.strip_html_and_bracket_markup(html_sentence)

        forms = [_vocab_note.get_question()] + list(_vocab_note.get_forms())
        forms = ex_sequence.remove_duplicates_while_retaining_order(forms)

        for form in forms:
            if form in clean_sentence:
                return clean_sentence.replace(form, f"""<span class="vocabInContext">{form}</span>""")
            else:
                form = kana_utils.get_conjugation_base(form)
                if form in clean_sentence:
                    return clean_sentence.replace(form, f"""<span class="vocabInContext">{form}</span>""")

        return clean_sentence


    highlighted_sentences = _vocab_note.get_user_highlighted_sentences()
    sentences = [(sent, "highlighted") for sent in highlighted_sentences]

    wanted_sentences = 10
    if len(sentences) < wanted_sentences:
        studying_sentences = [sent for sent in _vocab_note.get_sentences_studying() if sent not in highlighted_sentences]
        studying_sentences = studying_sentences[:(wanted_sentences - len(highlighted_sentences))]
        sentences += [(sent, "studying") for sent in studying_sentences]

        if len(highlighted_sentences) + len(studying_sentences) < wanted_sentences:
            any_sentences = [sent for sent in _vocab_note.get_sentences() if sent not in highlighted_sentences and sent not in studying_sentences]
            any_sentences = any_sentences[:(wanted_sentences - len(highlighted_sentences) - len(studying_sentences))]
            sentences += [(sent, "any") for sent in any_sentences]

    return f'''
             <div id="highlightedSentencesSection" class="page_section">
                <div class="page_section_title">sentences</div>
                <div id="highlightedSentencesList">
                    <div>
                        {newline.join([f"""
                        <div class="highlightedSentenceDiv">
                            <audio src="{_sentence.get_audio_path()}"></audio>
                            <div class="highlightedSentence {_class}">                            
                                <div class="sentenceQuestion clipboard">{format_sentence(_sentence.get_question())}</div>
                                <div class="sentenceAnswer"> {_sentence.get_answer()}</div>
                            </div>
                        </div>
                        """ for _sentence, _class in sentences])}
                    </div>
                </div>
            </div>
            '''



def render_highlighted_sentence_list(html: str, card: Card, _type_of_display: str) -> str:
    vocab_note = JPNote.note_from_card(card)

    if isinstance(vocab_note, VocabNote) and ui_utils.is_displaytype_displaying_answer(_type_of_display):
        highlighted_sentences_html = generate_highlighted_sentences_html_list(vocab_note)
        html = html.replace("##HIGHLIGHTED_SENTENCES##", highlighted_sentences_html)

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_highlighted_sentence_list)
