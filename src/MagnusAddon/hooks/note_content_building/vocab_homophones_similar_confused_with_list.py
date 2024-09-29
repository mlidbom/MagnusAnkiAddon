from anki.cards import Card
from aqt import gui_hooks

from ankiutils import app, ui_utils
from note import vocabnote
from note.jpnote import JPNote
from note.vocabnote import VocabNote
from sysutils import ex_sequence
from sysutils.ex_str import newline

def _create_classes(_vocab: VocabNote) -> str:
    tags = list(_vocab.priority_spec().tags)
    tags.sort()
    classes = " ".join([f"""common_ness_{prio}""" for prio in tags])
    classes += f""" {_vocab.priority_spec().priority_string}"""
    classes += " " + _vocab.get_meta_tags()
    return classes


def render_vocab_list(vocab_list: list[VocabNote], title:str) -> str:
    return f'''
             <div id="homophonesDiv" class="page_section">
                <div class="page_section_title">{title}</div>
                <div class="vocabHomophonesList">
                    <div>
                        {newline.join([f"""
                        <div class="homophone {_create_classes(_vocab_note)}">
                            <audio src="{_vocab_note.get_primary_audio_path()}"></audio><a class="play-button"></a>
                            <span class="question clipboard">{_vocab_note.get_question()}</span>                            
                            {_vocab_note.get_meta_tags_html()}
                            <span class="meaning"> {_vocab_note.get_answer()}</span>
                        </div>
                        """ for _vocab_note in vocab_list])}
                    </div>
                </div>
            </div>
            '''


def generate_homophones_html_list(_vocab_note: VocabNote, forms_to_ignore:set[VocabNote]) -> str:
    homophones = ex_sequence.flatten([app.col().vocab.with_reading(reading) for reading in _vocab_note.get_readings()])
    homophones = [homophone for homophone in homophones if homophone not in forms_to_ignore]
    homophones = vocabnote.sort_vocab_list_by_studying_status(homophones)

    return render_vocab_list(homophones, "homophones") if homophones else ""

def generate_similar_meaning_html_list(_vocab_note: VocabNote) -> str:
    similar = ex_sequence.flatten([app.col().vocab.with_question(question) for question in _vocab_note.get_related_similar_meaning()])
    similar = vocabnote.sort_vocab_list_by_studying_status(similar)

    return render_vocab_list(similar, "similar") if similar else ""

def generate_confused_with_html_list(_vocab_note: VocabNote) -> str:
    confused_with = ex_sequence.flatten([app.col().vocab.with_form(question) for question in _vocab_note.get_related_confused_with()])
    confused_with = vocabnote.sort_vocab_list_by_studying_status(confused_with)

    return render_vocab_list(confused_with, "confused_with") if confused_with else ""

def generate_ergative_twin_html(_vocab_note: VocabNote) -> str:
    ergative_twin = app.col().vocab.with_form(_vocab_note.get_related_ergative_twin())
    return render_vocab_list(ergative_twin, "ergative twin") if ergative_twin else ""

def generate_derived_from(_vocab_note: VocabNote) -> str:
    ergative_twin = app.col().vocab.with_form(_vocab_note.get_related_derived_from())
    return render_vocab_list(ergative_twin, "derived from") if ergative_twin else ""

def render_homophones_html_list(html: str, card: Card, _type_of_display: str) -> str:
    vocab_note = JPNote.note_from_card(card)

    if isinstance(vocab_note, VocabNote) and ui_utils.is_displaytype_displaying_answer(_type_of_display):
        #forms list
        forms = ex_sequence.flatten([app.col().vocab.with_question(reading) for reading in vocab_note.get_forms()])
        forms = [form for form in forms if form.get_id() != vocab_note.get_id()]
        forms = vocabnote.sort_vocab_list_by_studying_status(forms)
        html = html.replace("##DERIVED_FROM##", generate_derived_from(vocab_note))
        html = html.replace("##FORMS_LIST##", render_vocab_list([vocab_note] + forms, "forms") if forms else "")

        forms_set = set(forms) | {vocab_note}

        html = html.replace("##ERGATIVE_TWIN##", generate_ergative_twin_html(vocab_note))
        html = html.replace("##HOMOPHONES_LIST##", generate_homophones_html_list(vocab_note, forms_set))
        html = html.replace("##SIMILAR_MEANING_LIST##", generate_similar_meaning_html_list(vocab_note))
        html = html.replace("##CONFUSED_WITH_LIST##", generate_confused_with_html_list(vocab_note))

        html = html.replace("##VOCAB_META_TAGS_HTML##", vocab_note.get_meta_tags_html())
        html = html.replace("##VOCAB_CLASSES##", _create_classes(vocab_note))

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_homophones_html_list)
