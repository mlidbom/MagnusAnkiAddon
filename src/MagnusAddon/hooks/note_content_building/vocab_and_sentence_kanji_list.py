from anki.cards import Card
from aqt import gui_hooks

from ankiutils import ui_utils
from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_str
from viewmodels.kanji_list import sentence_kanji_list_viewmodel


def render_kanji_list(html:str, card: Card, _type_of_display:str) -> str:
    if not ui_utils.is_displaytype_displaying_answer(_type_of_display):
        return html

    note = JPNote.note_from_card(card)
    kanjis:list[str] = []

    if isinstance(note, VocabNote):
        kanjis = note.extract_main_form_kanji()
    elif isinstance(note, SentenceNote):
        kanjis = note.extract_kanji()
    else:
        return html

    list_html = ""
    if kanjis:
        viewmodel = sentence_kanji_list_viewmodel.create(kanjis)

        list_html += f"""
<div id="kanji_list" class="page_section">
    <div class="page_section_title">kanji</div>
{ex_str.newline.join(f'''
    <div class="kanji_item {" ".join(kanji.kanji.get_meta_tags())}">
        <div class="kanji_main">
            <span class="kanji_kanji clipboard">{kanji.question()}</span>
            <span class="kanji_readings">{kanji.readings()}</span>
            <span class="kanji_answer">{kanji.answer()}</span>        
        </div>
        <div class="kanji_mnemonic">{kanji.mnemonic()}</div>
    </div>
''' for kanji in viewmodel.kanji_list)}
</div>
        """

    html = html.replace("##KANJI_LIST##", list_html)


    return html


def init() -> None:
    gui_hooks.card_will_show.append(render_kanji_list)