from anki.cards import Card
from aqt import gui_hooks

from ankiutils import ui_utils
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.radicalnote import RadicalNote
from sysutils import ex_str
from viewmodels.kanji_list import sentence_kanji_list_viewmodel


def render_kanji_list(html:str, card: Card, _type_of_display:str) -> str:
    if not ui_utils.is_displaytype_displaying_answer(_type_of_display):
        return html

    from ankiutils import app
    note = JPNote.note_from_card(card)
    kanjis:list[str] = []

    if isinstance(note, KanjiNote):
        kanjis = [n.get_question() for n in app.col().kanji.with_radical(note.get_question())]
    elif isinstance(note, RadicalNote):
        kanjis = [n.get_question() for n in app.col().kanji.with_radical(note.get_question())] if note.get_question() else []
    else:
        return html

    if kanjis:
        viewmodel = sentence_kanji_list_viewmodel.create(kanjis)

        list_html = f"""
<div id="kanji_list" class="page_section">
    <div class="page_section_title">kanji</div>
{ex_str.newline.join(f'''
    <div class="kanji_item">
        <span class="kanji_kanji clipboard">{kanji.question()}</span>
        <span class="kanji_readings">{kanji.readings()}</span>
        <span class="kanji_answer">{kanji.answer()}</span>        
    </div>
    <div class="kanji_mnemonic">{kanji.mnemonic()}</div>
''' for kanji in viewmodel.kanji_list)}
</div>
        """

    html = html.replace("##KANJI_LIST##", list_html)

    return html


def init() -> None:
    gui_hooks.card_will_show.append(render_kanji_list)