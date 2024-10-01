from anki.cards import Card
from aqt import gui_hooks

from ankiutils import ui_utils
from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_sequence, ex_str, kana_utils
from sysutils.ex_str import newline


def generate_highlighted_sentences_html_list(_vocab_note: VocabNote) -> str:
    forms = [_vocab_note.get_question()] + list(_vocab_note.get_forms())
    forms = ex_sequence.remove_duplicates_while_retaining_order(forms)
    primary_form = _vocab_note.get_question_without_noise_characters()
    secondary_forms = [form for form in forms if form != primary_form]
    secondary_forms_conjugation_base_form = [kana_utils.get_conjugation_base(form) for form in secondary_forms]
    conjugation_base_form = kana_utils.get_conjugation_base(primary_form)

    def format_sentence(html_sentence: str) -> str:
        clean_sentence = ex_str.strip_html_and_bracket_markup(html_sentence)

        def create_form_class(_form:str) -> str:
            return "primaryForm" if _form == primary_form else "secondaryForm"


        for form in forms:
            if form in clean_sentence:
                clean_sentence = clean_sentence.replace(form, f"""<span class="vocabInContext {create_form_class(form)}">{form}</span>""")
            else:
                _conjugation_base_form = kana_utils.get_conjugation_base(form)
                if _conjugation_base_form in clean_sentence:
                    clean_sentence = clean_sentence.replace(_conjugation_base_form, f"""<span class="vocabInContext {create_form_class(form)}">{_conjugation_base_form}</span>""")

        return clean_sentence

    def sort_sentences(_sentences:list[SentenceNote]) -> list[SentenceNote]:

        def contains_primary_form(_sentence:SentenceNote) -> int:
            clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())
            return 1 if conjugation_base_form in clean_sentence else 2

        def contains_secondary_form(_sentence:SentenceNote) -> int:
            clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())
            return 2 if any((_base_form in clean_sentence for _base_form in secondary_forms_conjugation_base_form)) else 1

        return sorted(_sentences, key=lambda x: (contains_primary_form(x) + contains_secondary_form(x), len(x.get_question())))

    highlighted_sentences = _vocab_note.get_user_highlighted_sentences()
    highlighted_sentences = sort_sentences(highlighted_sentences)
    sentences = [(sent, "highlighted") for sent in highlighted_sentences]

    wanted_sentences = 10
    if len(sentences) < wanted_sentences:
        studying_sentences = [sent for sent in _vocab_note.get_sentences_studying() if sent not in highlighted_sentences]
        studying_sentences = sort_sentences(studying_sentences)
        studying_sentences = studying_sentences[:(wanted_sentences - len(highlighted_sentences))]
        sentences += [(sent, "studying") for sent in studying_sentences]

        if len(highlighted_sentences) + len(studying_sentences) < wanted_sentences:
            any_sentences = [sent for sent in _vocab_note.get_sentences() if sent not in highlighted_sentences and sent not in studying_sentences]
            any_sentences = sort_sentences(any_sentences)
            any_sentences = any_sentences[:(wanted_sentences - len(highlighted_sentences) - len(studying_sentences))]
            sentences += [(sent, "any") for sent in any_sentences]

    return f'''
             <div id="highlightedSentencesSection" class="page_section">
                <div class="page_section_title">sentences</div>
                <div id="highlightedSentencesList">
                    <div>
                        {newline.join([f"""
                        <div class="highlightedSentenceDiv">
                            <audio src="{_sentence.get_audio_path()}"></audio><a class="play-button"></a>
                            <div class="highlightedSentence {_class}">                            
                                <div class="sentenceQuestion clipboard">{format_sentence(_sentence.get_question())}</div>
                                <div class="sentenceAnswer"> {_sentence.get_answer()}</div>
                            </div>
                        </div>
                        """ for _sentence, _class in sentences])}
                    </div>
                </div>
            </div>
            ''' if sentences else ""



def render_highlighted_sentence_list(html: str, card: Card, _type_of_display: str) -> str:
    vocab_note = JPNote.note_from_card(card)

    if isinstance(vocab_note, VocabNote) and ui_utils.is_displaytype_displaying_answer(_type_of_display):
        highlighted_sentences_html = generate_highlighted_sentences_html_list(vocab_note)
        html = html.replace("##HIGHLIGHTED_SENTENCES##", highlighted_sentences_html)

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_highlighted_sentence_list)
