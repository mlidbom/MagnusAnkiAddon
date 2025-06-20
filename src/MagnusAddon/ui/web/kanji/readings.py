from __future__ import annotations

from aqt import gui_hooks
from note.kanjinote import KanjiNote
from sysutils import kana_utils
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def render_katakana_onyomi(kanji_note: KanjiNote) -> str:
    on_readings_list = [kana_utils.hiragana_to_katakana(x) for x in kanji_note.get_reading_on_list_html()]
    on_readings = ", ".join(f"""<span class="clipboard">{reading}</span>""" for reading in on_readings_list)
    kun_readings = ", ".join(f"""<span class="clipboard">{reading}</span>""" for reading in kanji_note.get_reading_kun_list_html())
    nan_readings = ", ".join(f"""<span class="clipboard">{reading}</span>""" for reading in kanji_note.get_reading_nan_list_html())

    return f"""
     <span class="reading">{on_readings}</span> <span class="readingsSeparator">|</span>
     <span class="reading">{kun_readings}</span> <span class="readingsSeparator">|</span>
     <span class="reading">{nan_readings}</span>
"""



def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(KanjiNote, {"##KANJI_READINGS##": render_katakana_onyomi}).render)
