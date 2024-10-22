import re

from anki.cards import Card
from aqt import gui_hooks

from ankiutils import ui_utils
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.radicalnote import RadicalNote
from sysutils import ex_str, kana_utils
from viewmodels.kanji_list.sentence_kanji_viewmodel import KanjiViewModel

def render_kanji_list(html:str, card: Card, _type_of_display:str) -> str:
    if not ui_utils.is_displaytype_displaying_answer(_type_of_display):
        return html

    from ankiutils import app
    note = JPNote.note_from_card(card)
    kanjis:list[KanjiNote] = []
    kanji_readings: list[str] = []

    if isinstance(note, KanjiNote):
        kanjis = app.col().kanji.with_radical(note.get_question())
        kanji_readings = [ex_str.strip_html_markup(reading) for reading in note.get_readings()]
    elif isinstance(note, RadicalNote):
        kanjis = app.col().kanji.with_radical(note.get_question()) if note.get_question() else []
    else:
        return html

    if not kanjis:
        return html.replace("##KANJI_LIST##", "")

    def highlight_inherited_reading(text: str) -> str:
        for primary_reading in kanji_readings:
            text = re.sub(rf'\b{kana_utils.to_hiragana(primary_reading)}|{kana_utils.to_katakana(primary_reading)}\b', f"<inherited-reading>{primary_reading}</inherited-reading>", text)

        return text

    def prefer__studying_kanji(kan: KanjiNote) -> int:
        return 0 if kan.is_studying() else 1

    kanjis = [kan for kan in kanjis if kan != note]
    kanjis = sorted(kanjis, key=lambda kan: prefer__studying_kanji(kan))

    viewmodels = [KanjiViewModel(kanji) for kanji in kanjis]

    list_html = f"""
<div id="kanji_list" class="page_section">
    <div class="page_section_title">kanji</div>
{ex_str.newline.join(f'''
    <div class="kanji_item {" ".join(kanji.kanji.get_meta_tags())}">
        <div class="kanji_main">
            <span class="kanji_kanji clipboard">{kanji.question()}</span>
            <span class="kanji_readings">{highlight_inherited_reading(kanji.readings())}</span>
            <span class="kanji_answer">{kanji.answer()}</span>        
        </div>
        <div class="kanji_mnemonic">{kanji.mnemonic()}</div>
    </div>
''' for kanji in viewmodels)}
</div>
        """

    html = html.replace("##KANJI_LIST##", list_html)
    return html


def init() -> None:
    gui_hooks.card_will_show.append(render_kanji_list)