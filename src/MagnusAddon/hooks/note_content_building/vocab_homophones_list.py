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

def generate_vocab_html_list(_vocab_note: VocabNote) -> str:
    homophones = ex_sequence.flatten([app.col().vocab.with_reading(reading) for reading in _vocab_note.get_readings()])
    homophones = [homophone for homophone in homophones if homophone.get_id() != _vocab_note.get_id()]
    homophones = vocabnote.sort_vocab_list_by_studying_status(homophones)

    if not homophones:
        return ""

    homophones = [_vocab_note] + homophones

    return f'''
             <div id="homophonesDiv" class="page_section">
                <div class="page_section_title" >Homophones</div>
                <div class="vocabHomophonesList">
                    <div>
                        {newline.join([f"""
                        <div class="homophone {_create_classes(_vocab_note)}">
                            <span class="question clipboard">{_vocab_note.get_question()}</span>                            
                            {_vocab_note.get_meta_tags_html()}
                            <span class="meaning"> {_vocab_note.get_answer()}</span>
                        </div>
                        """ for _vocab_note in homophones])}
                    </div>
                </div>
            </div>
            '''

def render_homophones_html_list(html: str, card: Card, _type_of_display: str) -> str:
    vocab_note = JPNote.note_from_card(card)

    if isinstance(vocab_note, VocabNote) and ui_utils.is_displaytype_displaying_answer(_type_of_display):
        homophones_list_html = generate_vocab_html_list(vocab_note)
        html = html.replace("##HOMOPHONES_LIST##", homophones_list_html)

        html = html.replace("##VOCAB_META_TAGS_HTML##", vocab_note.get_meta_tags_html())
        html = html.replace("##VOCAB_CLASSES##", _create_classes(vocab_note))

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_homophones_html_list)
