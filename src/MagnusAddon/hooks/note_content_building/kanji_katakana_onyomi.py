from anki.cards import Card
from aqt import gui_hooks

from ankiutils import ui_utils
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from sysutils import kana_utils



def render_katakana_onyomi(html: str, card: Card, _type_of_display: str) -> str:
    if not ui_utils.is_displaytype_displaying_answer(_type_of_display):
        return html

    kanji_note = JPNote.note_from_card(card)

    if isinstance(kanji_note, KanjiNote):
        on_readings_list = [kana_utils.to_katakana(x) for x in kanji_note.get_reading_on_list_html()]
        on_readings = ", ".join(f"""<span class="clipboard">{reading}</span>""" for reading in on_readings_list)
        kun_readings = ", ".join(f"""<span class="clipboard">{reading}</span>""" for reading in kanji_note.get_reading_kun_list_html())
        nan_readings = ", ".join(f"""<span class="clipboard">{reading}</span>""" for reading in kanji_note.get_reading_nan_list_html())

        readings_html = f"""
         <span class="reading">{on_readings}</span> <span class="readingsSeparator">|</span>
         <span class="reading">{kun_readings}</span> <span class="readingsSeparator">|</span>
         <span class="reading">{nan_readings}</span>
"""

        html = html.replace("##KANJI_READINGS##", readings_html)

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_katakana_onyomi)
